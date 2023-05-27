from aiogram.utils import executor
from create_bot import dp
from aiogram import types
from handlers import admin, other
from handlers.client import consult_handlers
from handlers.client import startup_handlers
from handlers.client import application_form_handlers
from aiogram.contrib.middlewares.logging import LoggingMiddleware


async def on_startup(_):
    print('Bot has been started')

dp.middleware.setup(LoggingMiddleware())

startup_handlers.register_handlers_startup(dp)
consult_handlers.register_handlers_consult(dp)
application_form_handlers.register_handlers_form_info(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
