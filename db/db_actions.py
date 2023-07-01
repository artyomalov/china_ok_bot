from aiogram import Bot
from const import ADMIN_ID
from db.models import SubscribtionUserData
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import ApplicationFormUserData, SubscribtionUserData


async def get_db_user(model: ApplicationFormUserData | SubscribtionUserData,
                      session: AsyncSession,
                      id: int):
    '''
    Get user model fro database
    '''
    request = select(model).filter_by(
        user_id=id)
    user_request = await session.execute(request)
    user = user_request.scalar()
    return user


async def add_new_user_to_db(
        model: SubscribtionUserData | ApplicationFormUserData,
        session: AsyncSession,
        user: dict,
        bot: Bot):
    '''
    Add new user to corresponding db depend on db model type
    '''

    try:
        await session.execute(insert(model), [user])
        await session.commit()
    except Exception as error:
        print(error)
        await bot.send_message(id=ADMIN_ID, text=error)
        return error


async def delete_user_from_db(
        model: SubscribtionUserData | ApplicationFormUserData,
        session: AsyncSession,
        bot: Bot,
        id: int):

    '''
    Delete user to corresponding db depend on db model type
    '''

    try:
        query = delete(model).filter_by(user_id=id)
        await session.execute(query)
        await session.commit()
    except Exception as error:
        print(error)
        await bot.send_message(id=ADMIN_ID, text=error)
        return error


async def update_user_fill_form_count(
        model: ApplicationFormUserData,
        session: AsyncSession,
        bot: Bot,
        id: int,
        filled_form_count: int
):

    '''
    Update user to corresponding db depend on db model type
    '''

    try:
        query = update(model).filter_by(user_id=id).values(
            filled_form_count=filled_form_count)

        await session.execute(query)
        await session.commit()
    except Exception as error:
        print(error)
        await bot.send_message(id=ADMIN_ID, text=error)
        return error
