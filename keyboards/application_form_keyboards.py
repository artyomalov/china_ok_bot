from aiogram import types


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Fill form
kb_application_form = types.InlineKeyboardMarkup(row_width=1)
kb_cancel_application_form_restart = types.InlineKeyboardMarkup(row_width=2)
button_fill_application_form = types.InlineKeyboardButton(
    text='Заполнить заявку', callback_data='button_fill_application_form')
button_restart_startup_menu = types.InlineKeyboardButton(
    text='Главное меню', callback_data='restart_main_menu')
kb_application_form.add(button_fill_application_form)
kb_cancel_application_form_restart.add(
    button_fill_application_form, button_restart_startup_menu)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Cancel fill form
kb_cancel = types.InlineKeyboardMarkup(row_width=2)
button_cancel = types.InlineKeyboardButton(
    text='Отмена', callback_data='cancel_fsm')

kb_cancel.add(button_cancel)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Auto set name
kb_auto_set_name = types.InlineKeyboardMarkup(row_width=1)
button_auto_set_name = types.InlineKeyboardButton(
    text='Вставить из профиля', callback_data='button_auto_set_name')
kb_auto_set_name.add(button_auto_set_name, button_cancel)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Skip photo upload
kb_skip_three_photo_upload = types.InlineKeyboardMarkup(row_width=1)
kb_skip_two_photo_upload = types.InlineKeyboardMarkup(row_width=1)
kb_skip_one_photo_upload = types.InlineKeyboardMarkup(row_width=1)
button_skip_three_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_three')
button_skip_two_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_two')
button_skip_one_photo_upload = types.InlineKeyboardButton(
    text='Пропустить добавление фото', callback_data='skip_one')
kb_skip_three_photo_upload.add(button_skip_three_photo_upload, button_cancel)
kb_skip_two_photo_upload.add(button_skip_two_photo_upload, button_cancel)
kb_skip_one_photo_upload.add(button_skip_one_photo_upload, button_cancel)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Need branding
kb_need_branding = types.InlineKeyboardMarkup(row_width=2)
button_need_branding_yes = types.InlineKeyboardButton(
    'Да', callback_data='need_branding_yes')
button_need_branding_no = types.InlineKeyboardButton(
    'Нет', callback_data='need_branding_no')
kb_need_branding.add(button_need_branding_yes,
                     button_need_branding_no, button_cancel)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Skip adittional requests
kb_skip_additional_data = types.InlineKeyboardMarkup()
button_skip_aditional_data = types.InlineKeyboardButton(
    'Пропустить', callback_data='skip_aditional_requests')
kb_skip_additional_data.add(button_skip_aditional_data, button_cancel)
