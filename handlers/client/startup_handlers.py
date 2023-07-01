import texts
from aiogram import types, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router
from aiogram.filters import Command
from const import LOREM
from keyboards.startup_keyboard import kb_on_start, kb_on_start_subscribed
from db.db_actions import get_db_user
from db.models import SubscribtionUserData
from servises.error_service import error_service


startup_router = Router()


@startup_router.message(Command('start'))
async def on_start_handler(
    message: types.Message,
    session: AsyncSession,
    bot: Bot
):
    '''
        Handler runs after '/start' command has been executed.
        Resurns three keyboard buttons: 'консультации', 'каталоги,' 'заявки'.
    '''
    try:
        user = await get_db_user(
            model=SubscribtionUserData,
            session=session,
            id=message.from_user.id
        )
        if user is not None:
            await message.answer(
                text=texts.STARTUP_GREETING_TEXT,
                reply_markup=kb_on_start_subscribed
            )
            await message.delete()
        else:
            await message.answer(
                text=texts.STARTUP_GREETING_TEXT,
                reply_markup=kb_on_start
            )
            await message.delete()
    except Exception as error:
        await error_service(
            error=error,
            bot=bot,
            message=message,
            error_location='startup_handlers - on_start_handler'
        )
