from aiogram import types
from .common_keyboards import button_cancel


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Fill form
button_fill_application_form = types.InlineKeyboardButton(
    text='Заполнить заявку', callback_data='button_fill_application_form')


kb_application_form = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_fill_application_form]])


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


button_skip_aditional_data = types.InlineKeyboardButton(
    text='Пропустить', callback_data='dont_add_aditional_requests')

buttons_skip_additional_data = [[button_skip_aditional_data], [button_cancel]]

kb_skip_additional_data = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_skip_additional_data)
