from aiogram import types, Bot
from const import ADMIN_ID


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
            chat_id=ADMIN_ID,
            text=err_msg
        )
        await message.answer(text='Что-то пошло не так. \
                                        Пожалуйста, попробуйте позже')
    else:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=err_msg
        )
        await message.message.answer(text='Что-то пошло не так. \
                                        Пожалуйста, попробуйте позже')
        await message.answer()
