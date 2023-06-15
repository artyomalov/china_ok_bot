from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_consult = KeyboardButton(text='/Консультации')
button_catalogs = KeyboardButton(text='/Каталоги')
button_application_form = KeyboardButton(text='/Заявки')

kb = [[button_consult], [button_catalogs], [button_application_form]]
kb_on_start = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, keyboard=kb)
