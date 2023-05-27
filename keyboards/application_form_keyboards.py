from aiogram import types

kb_applicateion_form = types.InlineKeyboardMarkup(row_width=1)
button_fill_application_form = types.InlineKeyboardButton(
    text='Заполнить заявку', callback_data='button_fill_application_form')
kb_applicateion_form.add(button_fill_application_form)


kb_auto_set_name = types.InlineKeyboardMarkup(row_width=1)
button_auto_set_name = types.InlineKeyboardButton(
    text='Вставить из профиля', callback_data='button_auto_set_name')
kb_auto_set_name.add(button_auto_set_name)

kb_skip_photo_upload = types.InlineKeyboardMarkup(row_width=1)
button_skip_photo_upload = types.InlineKeyboardButton(text='Пропустить добавление фото', callback_data='button_skip_photo_upload')
kb_skip_photo_upload.add(button_skip_photo_upload)