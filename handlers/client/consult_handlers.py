from aiogram import types
from aiogram import Router
from aiogram.filters import Command, Text
from keyboards.consult_keyboards import kb_consult, kb_consult_order
from const import LOREM

base_consult_routrer = Router()
# BASE CONSULT HANDLER


@base_consult_routrer.message(Command('Консультации'))
async def base_consult_handler(message: types.Message):
    '''
        Returns base consult description and two inline buttons: button_base_consult, product_selection_consult
    '''
    await message.answer(text=f'Консультации\n{LOREM}', reply_markup=kb_consult)
    await message.delete()


# BASE CONSULT CALLBACK
@base_consult_routrer.callback_query(Text('base_consult_callback'))
async def base_consult_callback(callback: types.CallbackQuery):
    await callback.message.answer(text=LOREM, reply_markup=kb_consult_order)
    await callback.answer()


# PRODUCT_SELECTION_CALLBACK
@base_consult_routrer.callback_query(Text('product_selection_callback'))
async def product_selection_callback(callback: types.CallbackQuery):
    await callback.message.answer(text=LOREM, reply_markup=kb_consult_order)
    await callback.answer()


# CONSULT ORDER CALLBACK
async def oreder_callback():
    pass
