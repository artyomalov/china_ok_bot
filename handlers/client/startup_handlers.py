from aiogram import types
from aiogram.dispatcher import Dispatcher
from texts import LOREM
from keyboards.startup_keyboard import kb_on_start

async def on_start_handler(message: types.Message):
    '''
        Handler runs after '/start' command has been executed. Resurns three keyboard buttons: 'консультации', 'каталоги,' 'заявки'.
    '''
    await message.answer(text=LOREM, reply_markup=kb_on_start)
    await message.delete()


def register_handlers_startup(dp: Dispatcher):
    dp.register_message_handler(on_start_handler, commands=['start', 'help'])