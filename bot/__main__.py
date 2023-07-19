import asyncio
import logging
import sys
import datetime
import servises.clear_notify_subscriber_servise as clear_notify_subscriber
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middleware import DbSessionMiddleware
from config_reader import config
from handlers.startup_handlers import startup_router
from handlers.consult_handlers import consult_router
from handlers.application_form_handlers import form_router
from handlers.catalog_handlers import catalog_router


async def main() -> None:

    engine = create_async_engine(
        url=config.db_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=config.bot_token.get_secret_value())

    await bot.set_my_commands(
        [BotCommand(command='start', description='Старт')],
        scope=BotCommandScopeDefault())

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    await bot.delete_webhook()
    scheduler.add_job(clear_notify_subscriber,
                      trigger='cron',
                      hour=datetime.datetime.now(
                      ).hour,
                      minute=datetime.datetime.now().minute + 1,
                      start_date=datetime.datetime.now(),
                      kwargs={'bot': bot, 'async_session': sessionmaker}
                      )
    scheduler.start()

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
