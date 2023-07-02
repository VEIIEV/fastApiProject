from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from security import user_schemas, depend, user_model
from security.user_model import User
from security.user_schemas import UserInDB


async def get_user(username: str, session: AsyncSession = Depends(get_session)) -> UserInDB:
    result = await session.execute(select(User).where(User.username == username))
    # .scalar() возвращает один результат или поднимает ошибку MultipleResultsFound
    return result.scalar()


async def get_user_by_id(id: int, session: AsyncSession) -> UserInDB:
    result = await session.execute(select(User).where(User.id == id))
    print(result)
    return result.scalar()


async def get_user_by_username(username: str, session: AsyncSession) -> UserInDB:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar()


async def create_user(user: user_schemas.CreateUser, session: AsyncSession):
    user.password = depend.get_password_hash(user.password)
    db_user = user_model.User(username=user.username,
                              hashed_password=user.password,
                              is_active=True,
                              salary=user.salary,
                              next_promotion=user.next_promotion)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return True
