from aiogram import types


# CONSULT KEYBOARD
button_base_consult = types.InlineKeyboardButton(
    text='Базовая консультация', callback_data='base_consult_callback')
button_product_selection_consult = types.InlineKeyboardButton(
    text='Подбор товара', callback_data='product_selection_callback')

kb_consult = types.InlineKeyboardMarkup(row_width=2)
kb_consult.add(button_base_consult, button_product_selection_consult)


# BASE CONSULT ORDER BUTTON
button_consult_order = types.InlineKeyboardButton(
    text='Заказать', callback_data='order_consult_callback')


kb_consult_order = types.InlineKeyboardMarkup(row_width=1)
kb_consult_order.add(button_consult_order)
