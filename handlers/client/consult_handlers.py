from aiogram import types, F, Bot
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.consult_keyboards import\
    kb_consult,\
    kb_consult_order,\
    kb_pay_consult
from const import ERROR_MESSAGE, LOREM
from keyboards.common_keyboards import\
    kb_cancel,\
    kb_cancel_application_form_restart
from keyboards.startup_keyboard import kb_on_start, kb_on_start_subscribed
from config_reader import config
from servises.cancel_fsm_service import cancel_fill_form_service
from google_sheets_connect import add_data_to_gsheets
from servises.error_service import error_service
from servises.get_time_service import get_time
from servises.send_invoice_service import send_invoice_handler
from servises.select_kb_service import select_kb_service
consult_router = Router()


class FSMFormConsult(StatesGroup):
    question_description = State()
    consultation_type = State()


@consult_router.callback_query(Text('cancel_fsm'))
async def cancel_consult_fsm(
    callback: types.callback_query,
    state: FSMContext
):
    await cancel_fill_form_service(
        callback=callback, state=state,
        keyboard=kb_cancel_application_form_restart
    )


@consult_router.callback_query(Text('restart_main_menu'))
async def restart_main_menu(callback: types.CallbackQuery):
    await callback.message.answer(text='OK', reply_markup=kb_on_start)
    await callback.answer()


@consult_router.message(Text('Консультации'))
async def base_consult_handler(message: types.Message):
    '''
    Returns base consult description and two inline buttons:
    button_base_consult, product_selection_consult
    '''
    await message.answer(
        text=f'Консультации\n{LOREM}',
        reply_markup=kb_consult)
    await message.delete()


# CONSULT TYPE CALLBACK
@consult_router.callback_query(Text(startswith='consult_select'))
async def consult_callback(
    callback: types.CallbackQuery,
    state: FSMContext
):
    async def consult_handler(consult_type: str):
        '''
        supporting function needed to simplify code and avoid code duplication
        sets type of FSM.consultation_type(base_consult or product_selection)
        '''
        await state.set_state(FSMFormConsult.consultation_type)
        await state.update_data(consultation_type=consult_type)
        await callback.message.answer(text=LOREM, reply_markup=kb_consult_order)
        await callback.answer()
    if callback.data == 'consult_select_base_callback':
        await consult_handler(consult_type='base_consult')
    elif callback.data == 'consult_select_product_selection_callback':
        await consult_handler(consult_type='product_selection')
    else:
        await callback.message.answer(
            text='Пожалуйста выберете один из указаных вариантов'
        )


# BASE CONSULT ORDER CALLBACK
@consult_router.callback_query(Text('order_consult_callback'))
async def get_description_callback_fsm(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await state.set_state(FSMFormConsult.question_description)
    await callback.message.answer(
        text='ПОЖАЛУЙСТА ОИШИТЕ СУТЬ ВОПРОСА',
        reply_markup=kb_cancel
    )
    await callback.answer()


@consult_router.message(FSMFormConsult.question_description)
async def order_consult_fsm(message: types.Message, state: FSMContext):
    await state.update_data(question_description=message.text)
    await message.answer(

        text='Спасибо. Что бы перейти к форме оплаты пожалуйста нажмите\
              кнопку оплатить. Ответным сообщением Вы получите счёт на\
              оплату. Вы сможете указать Ваше имя и контактные данные\
              на этапе оплаты. После успешной оплаты\
              менеджер свяжется с Вами в течение часа.',

        reply_markup=kb_pay_consult
    )


@consult_router.callback_query(Text(text='pay_consult'))
async def send_invoice(
        callback: types.CallbackQuery,
        state: FSMContext, bot: Bot
):

    data = await state.get_data()
    provider_token = config.payment_token.get_secret_value(),
    token = f'{provider_token[0]}'

    if data.get('consultation_type') == 'base_consult':
        await send_invoice_handler(
            callback_chat_id=callback.from_user.id,
            bot=bot,
            title='ЗАКАЗ БАЗОВОЙ КОНСУЛЬТАЦИИ',
            description='БАЗОВАЯ КОНСУЛЬТАЦИЯ И ЕЁ ОПИСАНИЕ,\
                  ЕСЛИ ОНО НЕОБХОДИМО',
            payload='consult',
            token=token,
            label_data='Базовая консультация',
            amount=200000
        )

    else:
        await send_invoice_handler(
            callback_chat_id=callback.from_user.id,
            bot=bot,
            payload='consult',
            title='ЗАКАЗ ПОДБОРА ТОВАРА',
            description='ПОДБОР ТОВАРА И ЕГО ОПИСАНИЕ,\
                  ЕСЛИ НЕОБХОДИМО',
            token=token,
            label_data='Подбор товара',
            amount=400000
        )


@consult_router.pre_checkout_query(F.invoice_payload == "consult")
async def pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery,
    state: FSMContext,
    bot: Bot
):

    '''get data(name, email, phone number) from payment page'''

    try:
        data = await state.get_data()
        question_description = data.get(
            'question_description',
            'Нет описания'
        )
        time = get_time()
        send_data = [[
            time,
            pre_checkout_query.order_info.name,
            pre_checkout_query.order_info.phone_number,
            pre_checkout_query.order_info.email,
            question_description,
        ]]
        add_data_to_gsheets(range='orders!A1:E1', send_data=send_data)
        await state.clear()
        await bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True
        )
    except Exception as error:
        await state.clear()
        await error_service(
            error=error,
            bot=bot,
            message=pre_checkout_query,
            error_location='consult_handlers - succsessfull_payment'
        )


@ consult_router.message(F.successful_payment.invoice_payload == "consult")
async def succsessfull_payment(message: types.Message, session: AsyncSession, bot: Bot):
    try:
        kb = await select_kb_service(session=session, id=message.from_user.id)
        await message.answer(
            text='Спасибо за оплату, менеджер свяжется с Вами в течение часа',
            reply_markup=kb
        )
    except Exception as error:
        await error_service(
            error=error,
            bot=bot,
            message=message,
            error_location='consult_handlers - succsessfull_payment -> '
        )
    # await bot.send_invoice(
    #     chat_id=callback.message.chat.id,
    #     title='Test order',
    #     description='Test descripiton',
    #     payload='Test payload',
    #     provider_token='401643678:TEST:0fa29bdf-0ccf-491e-9849-38a2f675ddfb',
    #     # provider_token=config.bot_token.get_secret_value(),
    #     currency='rub',
    #     prices=[
    #         types.LabeledPrice(
    #             label='Test label',
    #             amount=200000

    #         )
    #     ],
    #     # allow not allow anyone pay this bill if it will be resend to another user
    #     start_parameter='test',
    #     provider_data=None,
    #     photo_url=None,
    #     need_name=True,
    #     need_phone_number=True,
    #     need_email=True,
    #     send_phone_number_to_provider=False,
    #     send_email_to_provider=False,
    #     is_flexible=False,  # изменяется ли цена в зависимости от доставки или чего-то ещё
    #     # True, если нужно защитить пост от пересылки, копирования и т.д.
    #     protect_content=False,
    #     # если необходимо отправить счёт цитирую како-либо сообщение.
    #     reply_to_message_id=None,
    #     # позолит отправить счёт, даже если цитируемое сообщение не найдено.
    #     allow_sending_without_reply=True,
    #     # позволяет сформировать новую клавиатуру при отпавке сообщения пользователю. Первая кнопка должна быть оплатить.
    #     reply_markup=None,
    #     request_timeout=15  # timeout завпроса
    # )
