__all__=['get_subscribtion_time_service']

from db.db_actions import get_db_user
from db.models import SubscribtionUserData
from servises.count_rest_time_service import count_rest_time_service
from sqlalchemy.ext.asyncio import AsyncSession

async def get_subscribtion_time_service(
    session: AsyncSession,
    id: int,
):
    user: SubscribtionUserData = await get_db_user(
        model=SubscribtionUserData,
        session=session,
        id=id)
    if user is not None:
        return count_rest_time_service(user.subscribe_expire_time)
    else:
        return None