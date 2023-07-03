from datetime import datetime, timedelta, date

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    username: str
    is_active: bool = True
    salary: int | None = None
    next_promotion: date

class CreateUser(BaseUser):
    password: str = Field(max_length=30, min_length=6)


class UserInDB(BaseUser):
    id: int
    hashed_password: str

    class Config:
        # позволяет читать данные если это не dict, а модель из ORM
        # модель становится совместимой с ОРМ и может быть объявлена
        # в response_model=
        orm_mode = True
