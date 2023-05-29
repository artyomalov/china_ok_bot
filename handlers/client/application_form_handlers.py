from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils.markdown import text, bold
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import application_form_keyboards
from const import ALLOWED_PHONE_NUMBER_SYMBOLS, LOREM
from servises.return_user_answers_service import return_user_answers
from servises.run_startup_service import run_startup
from keyboards.startup_keyboard import kb_on_start

# SEND APPLICATION FROM'S INFO HANDLER


async def send_application_form_info_handler(message: types.Message):
    '''
        Returns application form description and one inline button. Button's text is "Заказать"
    '''
    msg = text(bold("Заполнение заявки и зачем это нужно"), LOREM, sep='\n')
    await message.answer(text=msg, reply_markup=application_form_keyboards.kb_application_form, parse_mode=types.ParseMode.MARKDOWN)
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


async def cancel_fsm(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.reset_state()
        await state.finish()
        await callback.message.answer(text=CANCEL_MESSAGE, reply_markup=application_form_keyboards.kb_cancel_application_form_restart)
        await callback.answer()
        return
    await state.finish()
    await callback.message.answer(text=CANCEL_MESSAGE, reply_markup=application_form_keyboards.kb_cancel_application_form_restart)
    await callback.answer()


async def restart_main_menu(callback: types.CallbackQuery):
    await callback.message.answer(text='OK', reply_markup=kb_on_start)
    await callback.answer()


async def start_fill_form_callback_fsm(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Пожалуйста, укажите имя', reply_markup=application_form_keyboards.kb_auto_set_name)
    await state.set_state(FSMForm.name)
    await callback.answer()


ASK_PHONE_NUMBER_MESSAGE = 'Спасибо! Теперь, пожалуйста укажите номер телефона'


async def auto_set_name_callback_fsm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.from_user.full_name)
    await callback.message.answer(ASK_PHONE_NUMBER_MESSAGE, reply_markup=application_form_keyboards.kb_cancel)
    await callback.answer()
    await state.set_state(FSMForm.phone_number)


async def set_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(ASK_PHONE_NUMBER_MESSAGE, reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.phone_number)


async def set_phone_number_fsm(message: types.Message, state: FSMContext):
    if set(message.text).issubset(ALLOWED_PHONE_NUMBER_SYMBOLS) or set(message.text) == ALLOWED_PHONE_NUMBER_SYMBOLS:
        await state.update_data(phone_number=message.text)
        await message.answer('Спасибо! Теперь, пожалуйста, укажите название товара', reply_markup=application_form_keyboards.kb_cancel)
        await state.set_state(FSMForm.product_name)
    else:
        await message.answer('номер телефона может состоять из цифр "0-9", круглых скобок() и знака "+"')


async def set_product_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer('Спасибо! Теперь, пожалуйста, прикрепите первую фотографию товара(1/3), либо нажмите на кнопку "пропустить", что бы пропустить добавление фотографий', reply_markup=application_form_keyboards.kb_skip_three_photo_upload)
    await state.set_state(FSMForm.product_photo_one)


async def upload_product_photo_one_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_one=message.photo[0].file_id)
    await message.answer('Спасибо! Теперь, пожалуйста, загрузите вторую фотографию товара(2/3) либо нажмите на конпку "пропустить", если Вы больше не хотите добавлять фотографии', reply_markup=application_form_keyboards.kb_skip_two_photo_upload)
    await state.set_state(FSMForm.product_photo_two)


async def upload_product_photo_two_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_two=message.photo[0].file_id)
    await message.answer('Спасибо! Теперь, пожалуйста, загрузите третью фотографию товара(3/3) либо нажмите на конпку "пропустить", если Вы больше не хотите добавлять фотографии', reply_markup=application_form_keyboards.kb_skip_one_photo_upload)
    await state.set_state(FSMForm.product_photo_three)

NOT_SET = 'Not set'
CHINESE_SOURSE_REQUEST = 'Пожалуйста, прикрепите ссылку на китайский источник'


async def skip_add_all_photo_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'skip_three':
        async with state.proxy() as data:
            data['product_photo_one'] = NOT_SET
            data['product_photo_two'] = NOT_SET
            data['product_photo_whree'] = NOT_SET
    if callback.data == 'skip_two':
        async with state.proxy() as data:
            data['product_photo_two'] = NOT_SET
            data['product_photo_whree'] = NOT_SET
    if callback.data == 'skip_one':
        async with state.proxy() as data:
            data['product_photo_whree'] = NOT_SET
    await callback.message.answer(CHINESE_SOURSE_REQUEST, reply_markup=application_form_keyboards.kb_cancel)
    await callback.answer()
    await state.set_state(FSMForm.chinese_source_link)


async def upload_product_photo_three_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_three=message.photo[0].file_id)
    await message.answer(CHINESE_SOURSE_REQUESTreply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.chinese_source_link)


async def set_chinese_source_link_fsm(message: types.Message, state: FSMContext):
    await state.update_data(chinese_source_link=message.text)
    await message.answer('Пожалуйста, укажите, нужно ли брендирование', reply_markup=application_form_keyboards.kb_need_branding)
    await state.set_state(FSMForm.need_branding)


async def set_has_branding_fsm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "need_branding_yes":
        await state.update_data(need_branding='Брендирование нужно')
    else:
        await state.update_data(need_branding='Брендирование не нужно')
    await callback.message.answer("Пожалуйста, укажите предполагаемый объём", reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.assumed_volume)
    await callback.answer()


async def set_assumed_volume_fsm(message: types.Message, state: FSMContext):
    await state.update_data(assumed_volume=message.text)
    await message.answer('Пожалуйста укажите предполагаемый бюджет', reply_markup=application_form_keyboards.kb_cancel)
    await state.set_state(FSMForm.assumed_budget)


async def set_assumed_budget_fsm(message: types.Message, state: FSMContext):
    await state.update_data(assumed_budget=message.text)
    await message.answer('Если есть какая-либо информация, которую Вы хотели бы добавить, пожалуйста, нажмите кнопку "Пропустить"', reply_markup=application_form_keyboards.kb_skip_additional_data)
    await state.set_state(FSMForm.additional_data)

ANSWERS_CHECK_REQUESTS = 'Спасибо за заполнение формы. Пожалуйста проверьте свои ответы'


async def skip_addittional_info_fsm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(additional_data='Дополнительная информация не указана')
    await callback.message.answer(ANSWERS_CHECK_REQUESTS)
    async with state.proxy() as data:
        await return_user_answers(data, callback.message)
    await state.finish()
    await callback.answer()


async def set_additional_data(message: types.Message, state: FSMContext):
    await state.update_data(additional_data=message.text)
    await message.answer(ANSWERS_CHECK_REQUESTS)
    async with state.proxy() as data:
        await return_user_answers(data, message)
    await state.finish()


def register_handlers_form_info(dp: Dispatcher):
    dp.register_message_handler(
        send_application_form_info_handler, commands=['Заявки']
    )
    dp.register_callback_query_handler(
        cancel_fsm, lambda callback: callback.data == 'cancel_fsm', state="*")

    dp.register_callback_query_handler(
        restart_main_menu, lambda callback: callback.data == 'restart_main_menu')

    dp.register_callback_query_handler(
        start_fill_form_callback_fsm, lambda callback: callback.data == 'button_fill_application_form')
    dp.register_callback_query_handler(
        auto_set_name_callback_fsm, lambda callback: callback.data == 'button_auto_set_name', state=FSMForm.name)
    dp.register_message_handler(set_name_fsm, state=FSMForm.name)
    dp.register_message_handler(
        set_phone_number_fsm, state=FSMForm.phone_number)
    dp.register_message_handler(
        set_product_name_fsm, state=FSMForm.product_name)
    dp.register_callback_query_handler(
        skip_add_all_photo_handler, lambda callback: callback.data and callback.data.startswith('skip'), state=[FSMForm.product_photo_one, FSMForm.product_photo_two, FSMForm.product_photo_three])
    dp.register_message_handler(
        upload_product_photo_one_fsm, state=FSMForm.product_photo_one, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(
        upload_product_photo_two_fsm, state=FSMForm.product_photo_two, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(upload_product_photo_three_fsm,
                                state=FSMForm.product_photo_three, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(
        set_chinese_source_link_fsm, state=FSMForm.chinese_source_link)
    dp.register_callback_query_handler(
        set_has_branding_fsm, lambda callback: callback.data and callback.data.startswith('need'), state=FSMForm.need_branding)
    dp.register_message_handler(
        set_assumed_volume_fsm, state=FSMForm.assumed_volume)
    dp.register_message_handler(
        set_assumed_budget_fsm, state=FSMForm.assumed_budget)
    dp.register_callback_query_handler(skip_addittional_info_fsm, lambda callback: callback.data ==
                                       'skip_aditional_requests', state=FSMForm.additional_data)
    dp.register_message_handler(
        set_additional_data, state=FSMForm.additional_data)
