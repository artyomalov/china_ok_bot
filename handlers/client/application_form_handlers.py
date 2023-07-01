import time
import texts
from aiogram import types, Bot, F
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards import application_form_keyboards
from const import ALLOWED_PHONE_NUMBER_SYMBOLS
from servises.count_rest_time_service import count_rest_time_service
from servises.get_time_service import get_time
from google_sheets_connect import add_data_to_gsheets
from db.models import ApplicationFormUserData
from keyboards.common_keyboards import kb_cancel, kb_send_data, \
    kb_cancel_application_form_restart
from db.db_actions import add_new_user_to_db, delete_user_from_db, get_db_user,\
    update_user_fill_form_count
from servises.select_kb_service import select_kb_service
from servises.convert_id_to_url_service import convert_id_to_url_service
from servises.check_data_service import check_data_service
from servises.cancel_fsm_service import cancel_fill_form_service
from servises.error_service import error_service


form_router = Router()


class FSMForm(StatesGroup):
    name = State()
    phone_number = State()
    product_name = State()
    product_photo_one = State()
    product_photo_two = State()
    product_photo_three = State()
    chinese_source_link = State()
    need_branding = State()
    assumed_volume = State()
    assumed_budget = State()
    additional_data = State()


@form_router.message(Text('Заявки'))
async def send_application_form_info_handler(message: types.Message):
    '''
        Returns application form description and one inline button.
        Button's text is "Заказать"
    '''
    await message.answer(
        text=texts.APPLICATION_FORM_DESCRIPTION,
        reply_markup=application_form_keyboards.kb_application_form)
    await message.delete()


@form_router.callback_query(Text('cancel_fsm'))
async def cancel_fsm(callback: types.CallbackQuery, state: FSMContext) -> None:
    await(cancel_fill_form_service(
        callback=callback,
        state=state,
        keyboard=kb_cancel_application_form_restart))


@form_router.callback_query(Text('restart_main_menu'))
async def restart_main_menu(
    callback: types.CallbackQuery,
    session: AsyncSession,
    bot: Bot
):
    try:
        kb = await select_kb_service(session=session, id=callback.from_user.id)
        await callback.message.answer(text='OK', reply_markup=kb)
        await callback.answer()
    except Exception as error:
        await error_service(
            error=error,
            bot=bot,
            message=callback.from_user.id,
            error_location='application_form_handlers - restart_main_menu'
        )


@form_router.callback_query(Text('button_fill_application_form'))
async def start_fill_form_callback_fsm(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        bot: Bot
):
    try:
        user: ApplicationFormUserData = await get_db_user(
            model=ApplicationFormUserData,
            session=session,
            id=callback.from_user.id
        )

        async def start_fill_form():
            '''
            Supporting function nedded to simplify code, starts form filling and
            used at two places(if user exists, but still not out of limits)
            and is user does not exist at database
            '''
            await callback.message.answer(
                text='Пожалуйста, укажите ФИО:',
                reply_markup=application_form_keyboards.kb_auto_set_name)
            await state.set_state(FSMForm.name)
            await callback.answer()

        if user != None:
            one_day_gone = True if (
                user.cant_fill_form_expire_time-time.time()) < 0 else False
            if (not one_day_gone and user.filled_form_count >= 3):
                rest_time = count_rest_time_service(
                    user.cant_fill_form_expire_time
                )
                await callback.message.answer(
                    text=f'''Вы заполнили масимальное число заявок на сегодня.
                    \nСнова заполнить заявку вы сможете через {rest_time}'''
                )
                await state.clear()
                return

            if (not one_day_gone and user.filled_form_count < 3):
                await start_fill_form()
                return

            if (one_day_gone):
                await delete_user_from_db(
                    model=ApplicationFormUserData,
                    session=session,
                    bot=bot,
                    id=callback.from_user.id
                )
        await start_fill_form()
    except Exception as error:
        await state.clear()
        await error_service(
            error=error,
            bot=bot,
            message=callback,
            error_location='application_form_handlers - start_fill_form_callback_fsm -> '
        )

ASK_PHONE_NUMBER_MESSAGE = 'Введите контактный номер телефона:'


@form_router.callback_query(FSMForm.name, Text('button_auto_set_name'))
async def auto_set_name_callback_fsm(callback: types.CallbackQuery,
                                     state: FSMContext):
    await state.update_data(name=callback.from_user.full_name)
    await callback.message.answer(
        text=ASK_PHONE_NUMBER_MESSAGE,
        reply_markup=kb_cancel)
    await callback.answer()
    await state.set_state(FSMForm.phone_number)


@form_router.message(FSMForm.name)
async def set_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(ASK_PHONE_NUMBER_MESSAGE, reply_markup=kb_cancel)
    await state.set_state(FSMForm.phone_number)


@form_router.message(FSMForm.phone_number)
async def set_phone_number_fsm(message: types.Message, state: FSMContext):
    if set(message.text).issubset(ALLOWED_PHONE_NUMBER_SYMBOLS) or set(message.text) == ALLOWED_PHONE_NUMBER_SYMBOLS:
        await state.update_data(phone_number=message.text)
        await message.answer('Наименование интересующего товара:', reply_markup=kb_cancel)
        await state.set_state(FSMForm.product_name)
    else:
        await message.answer('номер телефона может состоять из цифр "0-9", круглых скобок() и знака "+"')


@form_router.message(FSMForm.product_name)
async def set_product_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer(text=texts.REQUEST_PHOTO_DESCRIPTION)
    await message.answer(text=texts.REQUEST_PHOTO_ONE,
                         reply_markup=application_form_keyboards
                         .kb_skip_three_photo_upload)
    await state.set_state(FSMForm.product_photo_one)


# @form_router.message(FSMForm.product_photo_one)
# @form_router.message(F.document)
# @form_router.message(F.photo)
# async def upload_product_photo_one_fsm(
#         message: types.Message,
#         state: FSMContext,
#         bot: Bot):
#     print(message.document)
# РЕАЛИЗОВАТЬ ВОЗМОЖНОСТЬ ДОБАВЛЕНИЯ НЕСКОЛЬКИХ ФОТОГРАФИЙ.


@form_router.message(FSMForm.product_photo_one)
# @form_router.message(F.document)
# @form_router.message(F.photo)
async def upload_product_photo_one_fsm(
        message: types.Message,
        state: FSMContext,
        bot: Bot):

    id = str(message.document.file_id)\
        if message.document is not None else\
        str(message.photo[0].file_id)
    image_type = 'document' if message.document is not None else 'photo'
    url = await convert_id_to_url_service(bot=bot, file_id=id)
    url['image_type'] = image_type
    await state.update_data(product_photo_one=url)

    await message.answer(text=texts.REQUEST_PHOTO_TWO,
                         reply_markup=application_form_keyboards
                         .kb_skip_two_photo_upload)

    await state.set_state(FSMForm.product_photo_two)
NOT_SET = 'Not set'


@form_router.callback_query(Text(startswith='skip'))
async def skip_add_photo_handler(callback: types.CallbackQuery,
                                 state: FSMContext):

    if callback.data == 'skip_three':
        await state.update_data(product_photo_one=NOT_SET)
        await state.set_state(FSMForm.product_photo_two)
        await state.update_data(product_photo_two=NOT_SET)
        await state.set_state(FSMForm.product_photo_three)
        await state.update_data(product_photo_three=NOT_SET)
    if callback.data == 'skip_two':
        await state.set_state(FSMForm.product_photo_two)
        await state.update_data(product_photo_two=NOT_SET)
        await state.set_state(FSMForm.product_photo_three)
        await state.update_data(product_photo_three=NOT_SET)
    if callback.data == 'skip_one':
        await state.set_state(FSMForm.product_photo_three)
        await state.update_data(product_photo_three=NOT_SET)

    await callback.message.answer(
        text=texts.CHINESE_SOURSE_REQUEST,
        reply_markup=kb_cancel)
    await state.set_state(FSMForm.chinese_source_link)
    await callback.answer()


@form_router.message(FSMForm.product_photo_two)
async def upload_product_photo_two_fsm(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):
    id = str(message.document.file_id)\
        if message.document is not None else\
        str(message.photo[0].file_id)
    image_type = 'document' if message.document is not None else 'photo'
    url = await convert_id_to_url_service(bot=bot, file_id=id)
    url['image_type'] = image_type
    await state.update_data(product_photo_two=url)
    await message.answer(text=texts.REQUEST_PHOTO_THREE,
                         reply_markup=application_form_keyboards
                         .kb_skip_one_photo_upload)

    await state.set_state(FSMForm.product_photo_three)


@form_router.message(FSMForm.product_photo_three)
async def upload_product_photo_three_fsm(
        message: types.Message,
        state: FSMContext,
        bot: Bot
):
    id = str(message.document.file_id)\
        if message.document is not None else\
        str(message.photo[0].file_id)
    image_type = 'document' if message.document is not None else 'photo'
    url = await convert_id_to_url_service(bot=bot, file_id=id)
    url['image_type'] = image_type
    await state.update_data(product_photo_three=url)
    await message.answer(text=texts.CHINESE_SOURSE_REQUEST,
                         reply_markup=kb_cancel,
                         disable_web_page_preview=True
                         )
    await state.set_state(FSMForm.chinese_source_link)


@form_router.message(FSMForm.chinese_source_link)
async def set_chinese_source_link_fsm(
    message: types.Message,
    state: FSMContext
):
    user_text = message.text
    if user_text.startswith('https://') or user_text.startswith('www'):
        await state.update_data(chinese_source_link=message.text)
        await message.answer(
            text=texts.NEED_BRANDING,
            reply_markup=application_form_keyboards.kb_need_branding
        )
        await state.set_state(FSMForm.need_branding)
    else:
        await message.answer(text=texts.CHINESE_SOURSE_REQUEST_ERROR)


@form_router.callback_query(
    FSMForm.need_branding,
    Text(startswith='need_branding')
)
async def set_has_branding_fsm(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await state.update_data(need_branding='Брендирование нужно')
    if callback.data == "need_branding_yes":
        await state.update_data(need_branding='Брендирование нужно')
    else:
        await state.update_data(need_branding='Брендирование не нужно')
    await callback.message.answer(
        text=texts.ASSUMED_VOLUME_REQUEST,
        reply_markup=kb_cancel
    )
    await state.set_state(FSMForm.assumed_volume)
    await callback.answer()


@form_router.message(FSMForm.assumed_volume)
async def set_assumed_volume_fsm(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(assumed_volume=message.text)
    await message.answer(
        text=texts.ASSUMED_BUDGET_REQUEST,
        reply_markup=kb_cancel
    )
    await state.set_state(FSMForm.assumed_budget)


@form_router.message(FSMForm.assumed_budget)
async def set_assumed_budget_fsm(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(assumed_budget=message.text)
    await message.answer(
        text=texts.ADDITIONAL_INFO_REQUEST,
        reply_markup=application_form_keyboards
        .kb_skip_additional_data
    )
    await state.set_state(FSMForm.additional_data)


@form_router.callback_query(
    FSMForm.additional_data,
    Text('dont_add_aditional_requests')
)
async def skip_addittional_info_fsm(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await state.update_data(additional_data='Дополнительная информация не указана')
    await check_data_service(message=callback.message,
                             state=state,
                             keyboard=kb_send_data)
    await callback.answer()


@form_router.message(FSMForm.additional_data)
async def set_additional_data(message: types.Message, state: FSMContext):
    await state.update_data(additional_data=message.text)
    await check_data_service(message=message,
                             state=state,
                             keyboard=kb_send_data)


@form_router.callback_query(Text('send'))
async def send_data_to_google_sheets(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot
):
    try:
        id = callback.from_user.id
        kb = await select_kb_service(session=session, id=id)
        time = get_time()
        data = await state.get_data()
        send_data = []
        for item in data.values():
            if type(item) == dict:
                send_data.append(item.get('file_url'))
                continue
            send_data.append(item)
        # user_info_list = [item for item in data.values()]
        print(send_data)
        send_data = [[time] + send_data]
        add_data_to_gsheets(range='sales!A1:L1', send_data=send_data)

        user: ApplicationFormUserData = await get_db_user(
            model=ApplicationFormUserData,
            session=session,
            id=id
        )
        if user is not None:

            filled_form_count = user.filled_form_count+1
            await update_user_fill_form_count(
                model=ApplicationFormUserData,
                session=session,
                bot=bot,
                id=user.user_id,
                filled_form_count=filled_form_count,
            )

            await state.clear()
            await callback.message.answer(
                text=texts.FINISH_FILL_FORM_ANSWER,
                reply_markup=kb)
            await callback.answer()
            return

        new_user = {'user_id': id,
                    'name': data['name'],
                    'phone_number': data['phone_number'],
                    'filled_form_count': 1
                    }

        await add_new_user_to_db(
            model=ApplicationFormUserData,
            session=session,
            user=new_user,
            bot=bot
        )

        await state.clear()
        await callback.message.answer(
            text=texts.FINISH_FILL_FORM_ANSWER,
            reply_markup=kb
        )
        await callback.message.answer(
            text=texts.CONTACT_US,
            disable_web_page_preview=True,
        )
        await callback.message.answer(
            text=texts.GROUP_PROMOTION
        )
        await callback.answer()
    except Exception as error:
        await state.clear()
        await error_service(
            error=error,
            bot=bot,
            message=callback,
            error_location='application_form_handlers - send_data_to_google_sheets'
        )
