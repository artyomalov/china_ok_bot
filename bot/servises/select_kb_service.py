__all__ = ['select_kb_service']


from keyboards.startup_keyboard import kb_on_start, kb_on_start_subscribed
from db.db_actions import get_db_user
from db.models import SubscribtionUserData
from sqlalchemy.ext.asyncio import AsyncSession


async def select_kb_service(
        session: AsyncSession,
        id: int
):
    user = await get_db_user(
        model=SubscribtionUserData,
        session=session,
        id=id,

    )
    kb = kb_on_start if user is None else kb_on_start_subscribed

    return kb
