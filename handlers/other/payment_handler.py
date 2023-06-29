from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from config_reader import config


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Test order',
        description='Test descripiton',
        payload='Test payload',
        provider_token=config.bot_token.get_secret_value(),
        currency='rub',
        prices=[
            LabeledPrice(
                label='Test label',
                amount=1000

            )
        ],
        start_parameter='allow not allow anyone pay this bill if it will be resend to another user',
        provider_data=None,
        photo_url=None,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,  # изменяется ли цена в зависимости от доставки или чего-то ещё
        # True, если нужно защитить пост от пересылки, копирования и т.д.
        protect_content=False,
        # если необходимо отправить счёт цитирую како-либо сообщение.
        reply_to_message_id=None,
        # позолит отправить счёт, даже если цитируемое сообщение не найдено.
        allow_sending_without_reply=True,
        # позволяет сформировать новую клавиатуру при отпавке сообщения пользователю. Первая кнопка должна быть оплатить.
        reply_markup=None,
        request_timeout=15  # timeout завпроса
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    # ok true если товар, например, есть на складе.
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


async def succsessfull_payment(message: Message):
    msg = 'Спасибо за оплату'
    await message.answer(text=msg)
