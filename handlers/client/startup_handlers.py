from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from const import LOREM
from keyboards.startup_keyboard import kb_on_start


startup_router = Router()


@startup_router.message(Command('start'))
async def on_start_handler(message: types.Message):
    '''
        Handler runs after '/start' command has been executed. Resurns three keyboard buttons: 'консультации', 'каталоги,' 'заявки'.
    '''
    await message.answer(text=LOREM, reply_markup=kb_on_start)
    await message.delete()
