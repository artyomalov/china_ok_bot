import texts
import servises
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.startup_keyboard import kb_on_start, kb_on_start_subscribed
from db.db_actions import get_db_user
from db.models import SubscribtionUserData


startup_router = Router()


@startup_router.message(Command('start'))
async def on_start_handler(
    message: types.Message,
    session: AsyncSession,
    bot: Bot,
    state: FSMContext
):
    '''
        Handler runs after '/start' command has been executed.
        Resurns three keyboard buttons: 'консультации', 'каталоги,' 'заявки'.
    '''
    try:
        await state.clear()
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
        await servises.error_service(
            error=error,
            bot=bot,
            message=message,
            error_location='startup_handlers - on_start_handler'
        )
