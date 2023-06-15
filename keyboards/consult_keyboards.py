from aiogram import types


# CONSULT KEYBOARD
button_base_consult = types.InlineKeyboardButton(
    text='Базовая консультация', callback_data='base_consult_callback')
button_product_selection_consult = types.InlineKeyboardButton(
    text='Подбор товара', callback_data='product_selection_callback')

buttons_consult = [[button_base_consult], [button_product_selection_consult]]

kb_consult = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_consult)


# BASE CONSULT ORDER BUTTON
button_consult_order = types.InlineKeyboardButton(
    text='Заказать', callback_data='order_consult_callback')


kb_consult_order = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_consult_order]])
