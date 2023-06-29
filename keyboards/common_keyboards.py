from aiogram import types


button_cancel = types.InlineKeyboardButton(
    text='Отмена', callback_data='cancel_fsm')
kb_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])


button_send = types.InlineKeyboardButton(
    text='Отправить', callback_data='send')
buttons_send = [[button_send], [button_cancel]]
kb_send_data = types.InlineKeyboardMarkup(
    inline_keyboard=buttons_send)


button_restart_startup_menu = types.InlineKeyboardButton(
    text='Главное меню', callback_data='restart_main_menu')
kb_cancel_application_form_restart = types.InlineKeyboardMarkup(
    inline_keyboard=[[button_restart_startup_menu]])