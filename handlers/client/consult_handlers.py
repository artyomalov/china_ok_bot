from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.consult_keyboards import kb_consult, kb_consult_order
from texts import LOREM


# BASE CONSULT HANDLER
async def base_consult_handler(message: types.Message):
    '''
        Returns base consult description and two inline buttons: button_base_consult, product_selection_consult
    '''
    await message.answer(text=f'Консультации\n{LOREM}', reply_markup=kb_consult)
    await message.delete()

# BASE CONSULT CALLBACK
async def base_consult_callback(callback: types.CallbackQuery):
    await callback.message.answer(text=LOREM, reply_markup=kb_consult_order)
    await callback.answer()


# PRODUCT_SELECTION_CALLBACK
async def product_selection_callback(callback: types.CallbackQuery):
    await callback.message.answer(text=LOREM, reply_markup=kb_consult_order)
    await callback.answer()


# CONSULT ORDER CALLBACK
async def oreder_callback():
    pass


# REGISTER HANDLERS
def register_handlers_consult(dp: Dispatcher):
    dp.register_message_handler(
        base_consult_handler, commands=['Консультации'])
    dp.register_callback_query_handler(
        base_consult_callback, lambda callback: callback.data == 'base_consult_callback')
    dp.register_callback_query_handler(
        product_selection_callback, lambda callback: callback.data == 'product_selection_callback')
