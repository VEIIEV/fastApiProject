from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_session
from security.user_model import User
from security.user_schemas import UserInDB, CreateUser


async def get_user(username: str, session: AsyncSession = Depends(get_session)) -> UserInDB:
    result = await session.execute(select(User).where(User.username == username))
    # .scalar() возвращает один результат или поднимает ошибку MultipleResultsFound
    return result.scalar()
