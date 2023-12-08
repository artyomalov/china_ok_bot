__all__=['error_service']

from aiogram import types, Bot
from config_reader import config

async def error_service(
    error: Exception,
    message: types.Message | types.CallbackQuery,
    bot: Bot,
    error_location: str
):
    err_msg = f'{error_location} -> {error}'
    if (type(message) == types.Message or
            type(message) == types.PreCheckoutQuery):
        await bot.send_message(
            chat_id=config.admin_id.get_secret_value(),
            text=err_msg
        )
        await message.answer(text='Что-то пошло не так. \
                                        Пожалуйста, попробуйте позже')
    else:
        await bot.send_message(
            chat_id=config.admin_id.get_secret_value(),
            text=err_msg
        )
        await message.message.answer(text='Что-то пошло не так. \
                                        Пожалуйста, попробуйте позже')
        await message.answer()
