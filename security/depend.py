from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import get_session
from security import user_crud
from security.token_schemas import TokenData
from security.user_model import User
from security.user_schemas import UserInDB

# хеширование пароля, задача алгоритма
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# сравнение паролей
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# хеширование
def get_password_hash(password):
    return pwd_context.hash(password)


# аутентификация пользователя
async def authenticate_user(session: Annotated[AsyncSession, Depends(get_session)],
                      username: str, password: str):
    user = await user_crud.get_user_by_username(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# tokenUrl= путь для создания токена, auto_error=True - если пользователь не авторизован сразу поднимает ошибку
# нужно указывать полный путь с учётом роутера ААААААААААААААААААА
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='security/token', auto_error=True)

# создаем токен на основе полученных данных
def create_access_token(data: dict, expires_delta: timedelta| None=None):
    to_encode= data.copy()
    # задаем время удаления токента, как текущее время + expires_delta
    if expires_delta:
        expire= datetime.utcnow()+expires_delta
    else:
        expire= datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# получаем пользователя на основе данных в токена
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Annotated[AsyncSession, Depends(get_session)]) -> UserInDB:
    # сообщение с ошибкой
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_crud.get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user


# проверяем активен ли пользователь
async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
