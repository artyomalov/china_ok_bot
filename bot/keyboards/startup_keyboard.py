"""
Startap keyboard. Appears after /start command has been executed
"""


from aiogram import types

button_consult = types.KeyboardButton(text='Консультации')
button_catalogs = types.KeyboardButton(text='Каталоги')
button_subscribed = types.KeyboardButton(text='Проверить подписку')
button_application_form = types.KeyboardButton(text='Заявки')

kb = [[button_consult], [button_catalogs], [button_application_form]]
kb_subscribed = [[button_consult], [
    button_subscribed], [button_application_form]]

kb_on_start = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=kb,
    input_field_placeholder='Пожалуйста выберите интересующий Вас раздел'
)
kb_on_start_subscribed = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=kb_subscribed,
    input_field_placeholder='Пожалуйста выберите интересующий Вас раздел'
)
