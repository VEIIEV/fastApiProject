import datetime

from sqlalchemy import Column, String, Integer, Boolean, PickleType, DATETIME, DATE
from sqlalchemy.sql.functions import now

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    salary = Column(Integer, nullable=True)
    next_promotion = Column(DATE, default=datetime.date.today() + datetime.timedelta(days=180))
