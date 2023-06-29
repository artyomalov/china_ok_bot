from aiogram import types
from aiogram.fsm.context import FSMContext


async def check_data_service(
    message: types.Message,
    state: FSMContext,
    keyboard: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup,
):
    await message.answer('Спасибо за заполнение формы. \
                         Пожалуйста проверьте свои ответы')
    data = await state.get_data()
    for item in data.items():
        if str(item[0]).startswith('product_photo') and type(item[1]) is dict:
            if item[1]['image_type'] == 'photo':
                await message.answer_photo(photo=item[1].get('file_id'))
            else:
                await message.answer_document(document=item[1].get('file_id'))
            continue
        if item[1] == 'Not set':
            continue
        await message.answer(text=item[1])
    await message.answer(
        'Eсли все ответы верны, пожалуйста нажмите кнопку: \
                        "Отправить". Если же Вы хотите изменить свои ответы,\
                        пожалуйста нажмите кнопку "Отмена"',
        reply_markup=keyboard
    )
