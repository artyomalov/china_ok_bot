import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.types import BotCommand, BotCommandScopeDefault

from sqlalchemy.ext.asyncio import\
    create_async_engine,\
    async_sessionmaker,\
    AsyncSession

from middleware import DbSessionMiddleware
from config_reader import config

from handlers.client.startup_handlers import startup_router
from handlers.client.consult_handlers import consult_router
from handlers.client.application_form_handlers import form_router
from handlers.client.catalog_handlers import catalog_router
from aiogram.fsm.storage.memory import MemoryStorage


async def main() -> None:

    engine = create_async_engine(
        url=config.db_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=config.bot_token.get_secret_value())

    await bot.set_my_commands(
        [BotCommand(command='start', description='Старт')],
        scope=BotCommandScopeDefault())

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(startup_router)
    dp.include_router(consult_router)
    dp.include_router(catalog_router)
    dp.include_router(form_router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
