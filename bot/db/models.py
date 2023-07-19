from sqlalchemy import Column, Integer, VARCHAR,  BigInteger
from .base import Base
import time
from const import ONE_DAY_IN_SECONDS, ONE_MONTH_IN_SECONDS


def _get_fill_form_expire_time():
    return int(time.time()) + ONE_DAY_IN_SECONDS


def _get_subscribe_expire_time():
    return int(time.time()) + (ONE_MONTH_IN_SECONDS*3)


class ApplicationFormUserData(Base):
    __tablename__ = 'application_form_user_data'
    user_id = Column(BigInteger, unique=True,
                     primary_key=True, autoincrement=False)
    name = Column(VARCHAR(32), nullable=False)
    phone_number = Column(VARCHAR(40), nullable=False)
    filled_form_count = Column(Integer, nullable=False, default=1)
    cant_fill_form_expire_time = Column(
        BigInteger, default=_get_fill_form_expire_time)


class SubscribtionUserData(Base):
    __tablename__ = 'subscribtion_user_data'
    user_id = Column(BigInteger, unique=True,
                     primary_key=True, autoincrement=False)
    name = Column(VARCHAR(32), nullable=False)
    phone_number = Column(VARCHAR(40), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    subscribe_expire_time = Column(
        BigInteger, default=_get_subscribe_expire_time)
