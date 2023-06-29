from aiogram import types
from aiogram.fsm.context import FSMContext
from const import CANCEL_MESSAGE


async def cancel_fill_form_service(
    callback: types.CallbackQuery,
    state: FSMContext,
    keyboard: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup
):
    await state.clear()
    await callback.message.answer(
        text=CANCEL_MESSAGE,
        reply_markup=keyboard
    )
    await callback.answer()
