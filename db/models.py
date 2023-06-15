from sqlalchemy import Column, Integer, VARCHAR, DATE
from .base import Base


class ApplicationFormUserData(Base):
    __tablename__ = 'application_form_user_data'

    user_id = Column(VARCHAR, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)
    phone_number = Column(VARCHAR(40), nullable=False)
    filled_form_count = Column(Integer, nullable=False)

# !!!!!!!!!!!!!!!!!!Запросы к бд, добавить поля Дата. Узнать как написать дату.