from aiogram import types


# CONSULT KEYBOARD
button_base_consult = types.InlineKeyboardButton(
    text='Базовая консультация',
    callback_data='consult_select_base_callback'
)
button_product_selection_consult = types.InlineKeyboardButton(
    text='Подбор товара',
    callback_data='consult_select_product_selection_callback'
)

buttons_consult = [
    [button_base_consult],
    [button_product_selection_consult]
]

kb_consult = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_consult)


# BASE CONSULT ORDER BUTTON
button_consult_order_consult = types.InlineKeyboardButton(
    text='Заказать', callback_data='order_consult_callback')


kb_consult_order = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_consult_order_consult]])


# PAY FOR CONSULT
button_pay_for_consult = types.InlineKeyboardButton(
    text='Оплатить', callback_data='pay_consult')


kb_pay_consult = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_pay_for_consult]])
