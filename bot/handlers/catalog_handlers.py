import texts
import datetime
import servises
from aiogram import types, Router, Bot, F
from aiogram.filters import Text
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.catalog_keyboard import kb_subscribe
from keyboards.startup_keyboard import kb_on_start_subscribed
from servises.send_invoice_service import send_invoice_handler
from config_reader import config
from db.models import SubscribtionUserData
from db.db_actions import add_new_user_to_db


catalog_router = Router()


class FSMCatalog(StatesGroup):
    new_user = State()
    invite_link = State()


@catalog_router.message(Text('Проверить подписку'))
async def check_subscription_if_exists(message: types.Message, session: AsyncSession, bot: Bot):
    try:
        expire_time = await servises.get_subscribtion_time_service(
            session=session,
            id=message.from_user.id)
        if expire_time != None:
            await message.answer(text=f'Ваша подписка истекает через {expire_time}')
        else:
            await message.answer(text='У Вас нет подписки. \
Пожалуйста, перезапустите бота. Для этого нажмите кнопку "Меню" \
слева от поля ввода текста')
    except Exception as error:
        await servises.error_service(
            error=error,
            bot=bot,
            message=message,
            error_location='catalog_handlers - check_subscription_if_exists'
        )


@catalog_router.message(Text(text='Каталоги'))
async def show_catalog_description(
    message: types.Message,
    state: FSMContext
):
    '''
    Shows catalog\'s section description and subscribe button
    '''
    await state.clear()
    await message.answer(
        text=texts.CATALOG_DESCRIPTION,
        reply_markup=kb_subscribe)


@catalog_router.callback_query(Text(text='subscribe'))
async def pay_for_subscribtion(callback: types.CallbackQuery,
                               bot: Bot,
                               session: AsyncSession
                               ):
    '''
    Returns invoice to user.
    Invoice placed to separate microservice.
    if user already exists invoice will not be send
    '''

    provider_token = config.payment_token.get_secret_value(),
    token = f'{provider_token[0]}'
    try:
        expire_time = await servises.get_subscribtion_time_service(
            session=session,
            id=callback.from_user.id)
        if expire_time is not None:
            await callback.message.answer(text=f'Вы уже оформили подписку, \
                Ваша подписка истекает через {expire_time}')
            await callback.answer()
        else:
            await send_invoice_handler(
                callback_chat_id=callback.from_user.id,
                bot=bot,
                title='Оплата подписки',
                description='Оплата подписки',
                payload='subscription',
                token=token,
                label_data='Подписка на три месяца',
                amount=210000
            )
            await callback.answer()
    except Exception as error:
        await servises.error_service(
            error=error,
            bot=bot,
            message=callback,
            error_location='catalog_handlers - pay_for_subscribtion'
        )


@catalog_router.pre_checkout_query(F.invoice_payload == "subscription")
async def pre_checkout_query_catalog(
        pre_checkout_query: types.PreCheckoutQuery,
        bot: Bot,
        state: FSMContext):
    try:
        await bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True
        )
        new_user = {
            'user_id': pre_checkout_query.from_user.id,
            'name': pre_checkout_query.order_info.name,
            'phone_number':  pre_checkout_query.order_info.phone_number,
            'email':  pre_checkout_query.order_info.email,
        }
        await state.set_state(FSMCatalog.new_user)
        await state.update_data(new_user=new_user)
    except Exception as error:
        await servises.error_service(
            error=error,
            bot=bot,
            message=pre_checkout_query,
            error_location='catalog_handlers - pre_checkout_query_catalog'
        )


@catalog_router.message(F.successful_payment.invoice_payload == "subscription")
async def succsessfull_payment(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
    session: AsyncSession
):
    data = await state.get_data()
    new_user = data.get('new_user')

    await add_new_user_to_db(
        model=SubscribtionUserData,
        session=session,
        user=new_user,
        bot=bot
    )
    expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
    link = await bot.create_chat_invite_link(
        chat_id=config.chat_id.get_secret_value(),
        expire_date=expire_date,
        member_limit=1,
    )
    await state.set_state(FSMCatalog.invite_link)
    await state.update_data(invite_link=link.invite_link)
    print(link)
    await message.answer(text=f'Пожалуйста перейдите по ссылке, \
что бы подписаться на канал\n {link.invite_link}')
    await message.answer(
        text=texts.CATALOG_FINISH_MESSAGE,
        reply_markup=kb_on_start_subscribed,
        disable_web_page_preview=True
    )


@catalog_router.message(F.new_chat_members)
async def succsessfull_chat_join_request(
    message: types.Message,
    bot: Bot,
):
    user_name = message.from_user.username
    await bot.send_message(chat_id=config.admin_id.get_secret_value(), text=f'Новый подписчик в \
платном канале. \n{user_name}')
