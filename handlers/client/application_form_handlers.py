from aiogram import types
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from aiogram.utils.markdown import text, bold
from keyboards import application_form_keyboards, startup_keyboard
from const import ALLOWED_PHONE_NUMBER_SYMBOLS, LOREM
from servises.set_additional_data_service import set_additional_data_service
from keyboards.startup_keyboard import kb_on_start
from google_sheets_connect import cursor
from config_reader import config
from db.models import ApplicationFormUserData
form_router = Router()


@form_router.message(Command('Заявки'))
async def send_application_form_info_handler(message: types.Message):
    '''
        Returns application form description and one inline button. Button's text is "Заказать"
    '''
    msg = text(bold("Заполнение заявки и зачем это нужно"), LOREM, sep='\n')
    await message.answer(text=msg, reply_markup=application_form_keyboards.kb_application_form)
    await message.delete()


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


CANCEL_MESSAGE = 'Вы прервали заполнение формы. Если Вы хотиту начать заполнение заново нажмите на кнопку ниже, так же Вы можете заказать консультацию или подписаться на рассылку'


@form_router.callback_query(Text('cancel_fsm'))
async def cancel_fsm(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await callback.message.answer(text=CANCEL_MESSAGE, reply_markup=application_form_keyboards.kb_cancel_application_form_restart)
        await callback.answer()
        return
    await state.clear()
    await callback.message.answer(text=CANCEL_MESSAGE, reply_markup=application_form_keyboards.kb_cancel_application_form_restart)
    await callback.answer()


@form_router.callback_query(Text('restart_main_menu'))
async def restart_main_menu(callback: types.CallbackQuery):
    await callback.message.answer(text='OK', reply_markup=kb_on_start)
    await callback.answer()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@form_router.callback_query(Text('button_fill_application_form'))
async def start_fill_form_callback_fsm(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    id = callback.message.from_user.id
    request = select(ApplicationFormUserData).filter_by(
        user_id=id)
    user_request = await session.execute(request)
    user = user_request.scalar()
    # ОТТЕСТИРОВАТЬ ВРЕМЯ И ДАТУ.
    if user != None:
        one_day_gone = True if (
            datetime.today().date() - user.fill_form_date) > timedelta(days=1) else False
        if (not one_day_gone and user.filled_form_count >= 3):
            await callback.message.answer(text='Вы заполнили масимальное число заявок на сегодня')
            await state.clear()
            return
        if (not one_day_gone and user.filled_form_count < 3):
            await callback.message.answer('Пожалуйста, укажите имя', reply_markup=application_form_keyboards.kb_auto_set_name)
            await state.set_state(FSMForm.name)
            await callback.answer()
            return
        if (one_day_gone):
            query = delete(ApplicationFormUserData).filter_by(user_id=id)
            await session.execute(query)
            await session.commit()
    await callback.message.answer('Пожалуйста, укажите имя', reply_markup=application_form_keyboards.kb_auto_set_name)
    await state.set_state(FSMForm.name)
    await callback.answer()


ASK_PHONE_NUMBER_MESSAGE = 'Спасибо! Теперь, пожалуйста укажите номер телефона'


@form_router.callback_query(FSMForm.name, Text('button_auto_set_name'))
async def auto_set_name_callback_fsm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.from_user.full_name)
    await callback.message.answer(ASK_PHONE_NUMBER_MESSAGE, reply_markup=application_form_keyboards.kb_cancel)
    await callback.answer()
    await state.set_state(FSMForm.phone_number)


@form_router.message(FSMForm.name)
async def set_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(ASK_PHONE_NUMBER_MESSAGE, reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.phone_number)


@form_router.message(FSMForm.phone_number)
async def set_phone_number_fsm(message: types.Message, state: FSMContext):
    if set(message.text).issubset(ALLOWED_PHONE_NUMBER_SYMBOLS) or set(message.text) == ALLOWED_PHONE_NUMBER_SYMBOLS:
        await state.update_data(phone_number=message.text)
        await message.answer('Спасибо! Теперь, пожалуйста, укажите название товара', reply_markup=application_form_keyboards.kb_cancel)
        await state.set_state(FSMForm.product_name)
    else:
        await message.answer('номер телефона может состоять из цифр "0-9", круглых скобок() и знака "+"')


@form_router.message(FSMForm.product_name)
async def set_product_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer(text='Спасибо! Теперь, пожалуйста, прикрепите первую фотографию товара(1/3), либо нажмите на кнопку "пропустить", что бы пропустить добавление фотографий', reply_markup=application_form_keyboards.kb_skip_three_photo_upload)
    await state.set_state(FSMForm.product_photo_one)


@form_router.callback_query(FSMForm.product_photo_one, Text(startswith='skip'))
async def skip_add_all_photo_handler(callback: types.CallbackQuery, state: FSMContext):

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

    await callback.message.answer(CHINESE_SOURSE_REQUEST, reply_markup=application_form_keyboards.kb_cancel)
    await callback.answer()
    await state.set_state(FSMForm.chinese_source_link)


@form_router.message(FSMForm.product_photo_one)
async def upload_product_photo_one_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_one=message.photo[0].file_id)
    await message.answer(text='Спасибо! Теперь, пожалуйста, загрузите вторую фотографию товара(2/3) либо нажмите на конпку "пропустить", если Вы больше не хотите добавлять фотографии', reply_markup=application_form_keyboards.kb_skip_two_photo_upload)
    await state.set_state(FSMForm.product_photo_two)


@form_router.message(FSMForm.product_photo_two)
async def upload_product_photo_two_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_two=message.photo[0].file_id)
    await message.answer(text='Спасибо! Теперь, пожалуйста, загрузите третью фотографию товара(3/3) либо нажмите на конпку "пропустить", если Вы больше не хотите добавлять фотографии', reply_markup=application_form_keyboards.kb_skip_one_photo_upload)
    await state.set_state(FSMForm.product_photo_three)

NOT_SET = 'Not set'
CHINESE_SOURSE_REQUEST = 'Пожалуйста, прикрепите ссылку на китайский источник'


@form_router.message(FSMForm.product_photo_three)
async def upload_product_photo_three_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_three=message.photo[0].file_id)
    await message.answer(text=CHINESE_SOURSE_REQUEST, reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.chinese_source_link)


@form_router.message(FSMForm.chinese_source_link)
async def set_chinese_source_link_fsm(message: types.Message, state: FSMContext):
    user_text = message.text
    if user_text.startswith('https://') or user_text.startswith('www'):
        await state.update_data(chinese_source_link=message.text)
        await message.answer(text='Пожалуйста, укажите, нужно ли брендирование', reply_markup=application_form_keyboards.kb_need_branding)
        await state.set_state(FSMForm.need_branding)
    else:
        await message.answer(text='Пожалуйста укажите ссылку на сайт. Ссылка может начинаться с "https://" или c "www"')


@form_router.callback_query(FSMForm.need_branding, Text(startswith='need_branding'))
async def set_has_branding_fsm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(need_branding='Брендирование нужно')
    if callback.data == "need_branding_yes":
        await state.update_data(need_branding='Брендирование нужно')
    else:
        await state.update_data(need_branding='Брендирование не нужно')
    await callback.message.answer(text="Пожалуйста, укажите предполагаемый объём", reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.assumed_volume)
    await callback.answer()


@form_router.message(FSMForm.assumed_volume)
async def set_assumed_volume_fsm(message: types.Message, state: FSMContext):
    await state.update_data(assumed_volume=message.text)
    await message.answer(text='Пожалуйста укажите предполагаемый бюджет', reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.assumed_budget)


@form_router.message(FSMForm.assumed_budget)
async def set_assumed_budget_fsm(message: types.Message, state: FSMContext):
    await state.update_data(assumed_budget=message.text)
    await message.answer(text='Если есть какая-либо информация, которую Вы хотели бы добавить, пожалйуста укажите её, если же такой информации\
                          нет, пожалуйста, нажмите кнопку "Пропустить"', reply_markup=application_form_keyboards.kb_skip_additional_data)
    await state.set_state(FSMForm.additional_data)


@form_router.callback_query(FSMForm.additional_data, Text('skip_aditional_requests'))
async def skip_addittional_info_fsm(callback: types.CallbackQuery, state: FSMContext):
    await set_additional_data_service(message=callback.message,
                                      state=state,
                                      additional_data_text='Дополнительная информация не указана',
                                      keyboard=application_form_keyboards.kb_send_data_google_sheets)
    await callback.answer()


@form_router.message(FSMForm.additional_data)
async def set_additional_data(message: types.Message, state: FSMContext):
    await set_additional_data_service(message=message,
                                      state=state,
                                      additional_data_text=message.text,
                                      keyboard=application_form_keyboards.kb_send_data_google_sheets)


@form_router.callback_query(Text('send'))
async def send_data_to_google_sheets(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    id = callback.message.from_user.id
    time = datetime.today().strftime('%Y-%m-%d').replace('-', '/')
    data = await state.get_data()
    user_info_list = [item for item in data.values()]
    send_data = [[time] + user_info_list]
    cursor.append(
        spreadsheetId=config.sample_spreadsheet_id.get_secret_value(),
        range='sales!A1:L1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': send_data}
    ).execute()
    request = select(ApplicationFormUserData).filter_by(
        user_id=id)
    user_request = await session.execute(request)
    user = user_request.scalar()
    if user is not None:
        query = update(ApplicationFormUserData).filter_by(
            user_id=id).values(filled_form_count=user.filled_form_count+1)
        await session.execute(query)
        await session.commit()
        await state.clear()
        await callback.message.answer(text='Спасибо за заполнение заявки. Мы свяжемся с Вами в течение часа',
                                      reply_markup=startup_keyboard.kb_on_start)
        await callback.answer()
        return
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    await session.execute(insert(ApplicationFormUserData), [{'user_id': id,
                                                             'name': data['name'],
                                                             'phone_number':data['phone_number'],
                                                             'filled_form_count': 1
                                                             }])
    await session.commit()
    await state.clear()
    await callback.message.answer(text='Спасибо за заполнение заявки. Мы свяжемся с Вами в течение часа',
                                  reply_markup=startup_keyboard.kb_on_start)
    await callback.answer()
