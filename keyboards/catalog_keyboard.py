from aiogram import types

button_subscribe = types.InlineKeyboardButton(
    text='Оформить подписку', callback_data='subscribe'
)

kb_subscribe = types.InlineKeyboardMarkup(inline_keyboard=[[button_subscribe]])