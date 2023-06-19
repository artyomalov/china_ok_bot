from sqlalchemy import Column, Integer, VARCHAR, DATE, BigInteger
from .base import Base
from datetime import datetime

def _get_date():
    return datetime.today()


class ApplicationFormUserData(Base):
    __tablename__ = 'application_form_user_data'
    user_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=False)
    name = Column(VARCHAR(32), nullable=False)
    phone_number = Column(VARCHAR(40), nullable=False)
    filled_form_count = Column(Integer, nullable=False, default=1)
    fill_form_date = Column(DATE, default=_get_date)

# !!!!!!!!!!!!!!!!!!Запросы к бд, добавить поля Дата. Узнать как написать дату.
