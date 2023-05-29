async def return_user_answers(data, message):
        for item in data.items():
            if str(item[0]).startswith('product_photo') and item[1] != 'Not set':
                await message.answer_photo(photo=item[1])
                continue
            if item[1] == 'Not set':
                continue
            await message.answer(text=item[1])