__all__ = ['clear_notify_subscriber_servise']


import time
from aiogram import Bot
from sqlalchemy import select, delete
from db.models import SubscribtionUserData
from const import ONE_DAY_IN_SECONDS
from sqlalchemy.ext.asyncio import async_sessionmaker


async def clear_notify_subscriber_servise(
    bot: Bot,
    async_session: async_sessionmaker
):
    '''
    function delete user if his subscribtion time has been expired and send
    notification if his subscribtion time will expire in two days
    '''

    async with async_session() as session:
        async with session.begin():
            stmt = select(SubscribtionUserData)
            result = await session.execute(stmt)
            for subscriber in result.scalars():
                member = await bot.get_chat_member(
                    chat_id=-1001934317046,
                    user_id=subscriber.user_id)
                if (
                        member.status == 'administrator'
                        or member.status == 'creator'
                ):
                    return
                if subscriber.subscribe_expire_time < time.time():
                    req = delete(SubscribtionUserData).filter_by(
                        user_id=subscriber.user_id)
                    await bot.ban_chat_member(
                        chat_id=-1001934317046,
                        user_id=subscriber.user_id
                    )
                    await bot.unban_chat_member(
                        chat_id=-1001934317046,
                        user_id=subscriber.user_id
                    )
                    await bot.send_message(
                        chat_id=subscriber.user_id,
                        text='Ваша подписка на канал "China OK" истекла'
                    )
                    await session.execute(req)
                    await session.commit()
                    continue
                if ((subscriber.subscribe_expire_time - time.time())
                        < ONE_DAY_IN_SECONDS*2):
                    await bot.send_message(
                        chat_id=subscriber.user_id,
                        text='Ваша подписка на канал "CATALOGS"\
                              истекает через два дня'
                    )
                    continue
                continue
