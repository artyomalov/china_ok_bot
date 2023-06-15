
async def set_additional_data_service(message, state, additional_data_text, keyboard):
    await state.update_data(additional_data=additional_data_text)
    await message.answer('Спасибо за заполнение формы. Пожалуйста проверьте свои ответы')
    data = await state.get_data()
    for item in data.items():
        if str(item[0]).startswith('product_photo') and item[1] != 'Not set':
            await message.answer_photo(photo=item[1])
            continue
        if item[1] == 'Not set':
            continue
        await message.answer(text=item[1])
    await message.answer('Eсли все ответы верны, пожалуйста нажмите кнопку: "Отправить". Если же Вы хотите изменить свои ответы, пожалуйста нажмите кнопку "Отмена"',
                         reply_markup=keyboard)
