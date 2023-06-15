from aiogram import types


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Fill form
button_fill_application_form = types.InlineKeyboardButton(
    text='Заполнить заявку', callback_data='button_fill_application_form')
button_restart_startup_menu = types.InlineKeyboardButton(
    text='Главное меню', callback_data='restart_main_menu')

kb_application_form = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_fill_application_form]])
kb_cancel_application_form_restart = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_restart_startup_menu]])


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Cancel fill form
button_cancel = types.InlineKeyboardButton(
    text='Отмена', callback_data='cancel_fsm')

kb_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Auto set name
button_auto_set_name = types.InlineKeyboardButton(
    text='Вставить из профиля', callback_data='button_auto_set_name')
kb_auto_set_name = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_auto_set_name]])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Skip photo upload
button_skip_three_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_three')
button_skip_two_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_two')
button_skip_one_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_one')

kb_skip_three_photo_upload = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_skip_three_photo_upload]])
kb_skip_two_photo_upload = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_skip_two_photo_upload]])
kb_skip_one_photo_upload = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_skip_one_photo_upload]])


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Need branding
button_need_branding_yes = types.InlineKeyboardButton(
    text='Да', callback_data='need_branding_yes')
button_need_branding_no = types.InlineKeyboardButton(
    text='Нет', callback_data='need_branding_no')

buttons_need_branding = [[button_need_branding_yes], [button_need_branding_no]]

kb_need_branding = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_need_branding)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Skip adittional requests
button_skip_aditional_data = types.InlineKeyboardButton(
    text='Пропустить', callback_data='skip_aditional_requests')

buttons_skip_additional_data = [[button_skip_aditional_data], [button_cancel]]

kb_skip_additional_data = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_skip_additional_data)


button_send = types.InlineKeyboardButton(
    text='Отправить', callback_data='send')

buttons_send = [[button_send], [button_cancel]]

kb_send_data_google_sheets = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_send)
