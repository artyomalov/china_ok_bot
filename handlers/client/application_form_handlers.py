from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils.markdown import text, bold
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.application_form_keyboards import kb_applicateion_form, kb_auto_set_name, kb_skip_photo_upload
from texts import LOREM

# SEND APPLICATION FROM'S INFO HANDLER


async def send_application_form_info_handler(message: types.Message):
    '''
        Returns application form description and one inline button. Button's text is "Заказать"
    '''
    msg = text(bold("Заполнение заявки и зачем это нужно"), LOREM, sep='\n')
    await message.answer(text=msg, reply_markup=kb_applicateion_form, parse_mode=types.ParseMode.MARKDOWN)
    await message.delete()


class FSMForm(StatesGroup):
    name = State()
    phone_number = State()
    product_name = State()
    product_photo_one = State()
    product_photo_two = State()
    product_photo_three = State()
    chinese_source_link = State()
    need_branging = State()
    assumed_volume = State()
    assumed_budget = State()
    aditional_requests = State()


async def start_fill_form_callback_fsm(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Пожалуйста, укажите имя', reply_markup=kb_auto_set_name)
    await state.set_state(FSMForm.name)
    await callback.answer()


async def auto_set_name_callback_fsm(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.from_user.full_name)
    await callback.message.answer('Спасибо! Теперь, пожалуйста укажите номер телефона')
    await callback.answer()
    await state.set_state(FSMForm.phone_number)


async def set_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Спасибо! Теперь, пожалуйста, укажите номер телефона')
    await state.set_state(FSMForm.phone_number)


async def set_phone_number_fsm(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Спасибо! Теперь, пожалуйста, укажите название товара')
    await state.set_state(FSMForm.product_name)


async def set_product_name_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer('Спасибо! Теперь, пожалуйста, прикрепите первую фотографию товара(1/3)), либо нажмите на кнопку "пропустить", что бы пропустить добавление фотографий', reply_markup=kb_skip_photo_upload)
    await state.set_state(FSMForm.product_photo_one)


async def skip_add_all_photo_handler(callback: types.CallbackQuery, state: FSMContext):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>s')
    async with state.proxy() as data:
        data['product_photo_one'] = 'Not set'
        data['product_photo_two'] = 'Not set'
        data['product_photo_whree'] = 'Not set'
    await callback.message.answer('Пожалуйста, прикрепите ссылку на китайский источник')
    await state.set_state(FSMForm.chinese_source_link)


async def upload_product_photo_one_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_one=message.photo[0].file_id)
    await message.answer('Спасибо! Теперь, пожалуйста, загрузите вторую фотографию товара(2/3) либо нажмите на конпку "пропустить", что бы перейти к следующему шагу', reply_markup=kb_skip_photo_upload)
    await state.set_state(FSMForm.product_photo_two)


#переписать коллбэк так что бы парсить из него данные и в зависимости от услови перезависывать 1, 2 или 3 фотографии


async def upload_product_photo_two_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_two=message.photo[0].file_id)
    await message.answer('Спасибо! Теперь, пожалуйста, загрузите третью фотографию товара(3/3) либо нажмите на конпку "пропустить", что бы перейти к следующему шагу', reply_markup=kb_skip_photo_upload)
    await state.set_state(FSMForm.product_photo_three)


async def upload_product_photo_three_fsm(message: types.Message, state: FSMContext):
    await state.update_data(product_photo_three=message.photo[0].file_id)
    await message.answer('Пожалуйста, прикрепите ссылку на китайский источник')
    await state.set_state(FSMForm.chinese_source_link)


async def set_chinese_source_link_fsm(message: types.Message, state: FSMContext):
    await state.update_data(chinese_source_link=message.text)
    await message.answer('Пожалуйста, укажите, нужно ли брендирование')
    await state.set_state(FSMForm.need_branging)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Дописать ветвление на Да, нужно и Нет, не нужно


def register_handlers_form_info(dp: Dispatcher):
    dp.register_message_handler(
        send_application_form_info_handler, commands=['Заявки']
    )
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
        skip_add_all_photo_handler, lambda callback: callback.data == 'button_skip_photo_upload')

    dp.register_message_handler(
        upload_product_photo_one_fsm, state=FSMForm.product_photo_one, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(
        upload_product_photo_two_fsm, state=FSMForm.product_photo_two, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(upload_product_photo_three_fsm,
                                state=FSMForm.product_photo_three, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(
        set_chinese_source_link_fsm, state=FSMForm.chinese_source_link)
