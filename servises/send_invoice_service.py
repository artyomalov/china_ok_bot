from aiogram import types, Bot


async def send_invoice_handler(callback_chat_id: types.CallbackQuery,
                               bot: Bot,
                               title: str,
                               description: str,
                               payload: str,
                               token: str,
                               label_data: str,
                               amount: int
                               ):
    '''
    sends invoice to user
    '''
    await bot.send_invoice(
        chat_id=callback_chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=token,

        currency='rub',
        prices=[
            types.LabeledPrice(
                label=label_data,
                amount=amount

            )
        ],
        start_parameter='dont_resend',
        provider_data=None,
        photo_url=None,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        allow_sending_without_reply=True,
        request_timeout=15
    )
