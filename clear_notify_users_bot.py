import datetime
import time
import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import\
    create_async_engine,\
    async_sessionmaker
from config_reader import config
from sqlalchemy import select, delete
from db.models import SubscribtionUserData
from const import ONE_DAY_IN_SECONDS


async def delete_or_notify_subscriber(bot: Bot):
    '''
    function delete user if his subscribtion time has been expired and send
    notification if his subscribtion time will expire in two days
    '''
    engine = create_async_engine(
        url=config.db_url, echo=True)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            stmt = select(SubscribtionUserData)
            result = await session.execute(stmt)
            for subscriber in result.scalars():
                member = await bot.get_chat_member(
                    chat_id=-1001934317046,
                    user_id=subscriber.user_id)
                if member.is_chat_admin():
                    continue
                if subscriber.subscribe_expire_time < time.time():

                    req = delete(SubscribtionUserData).where(
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
                        text='Ваша подписка на канал China OK истекла'
                    )
                    await session.execute(req)
                    await session.commit
                    continue
                if ((subscriber.subscribe_expire_time - time.time())
                        < ONE_DAY_IN_SECONDS*2):
                    print('expire one two days')
                    await bot.send_message(
                        id=subscriber.user_id,
                        text='Ваша подписка на канал "название канала"\
                              истекает через два дня'
                    )
                    continue
                continue

    await engine.dispose()


async def main() -> None:

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # trigger = CronTrigger(year='*', month='*', day='*',
    #                       hour=12, minute=0, second=0)

    scheduler.add_job(delete_or_notify_subscriber,
                      trigger='cron',
                      hour=datetime.datetime.now(
                      ).hour,
                      minute=datetime.datetime.now().minute + 1,
                      start_date=datetime.datetime.now(),
                      kwargs={'bot': bot}
                      )
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
