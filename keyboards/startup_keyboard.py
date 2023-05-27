from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_consult = KeyboardButton('/Консультации')
button_catalogs = KeyboardButton('/Каталоги')
button_application_form = KeyboardButton('/Заявки')
kb_on_start = ReplyKeyboardMarkup(resize_keyboard=True)


kb_on_start.row(button_consult, button_catalogs, button_application_form)