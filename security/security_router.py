from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import settings
from db import get_session
from security import depend, user_crud
from security.depend import get_current_user
from security.user_schemas import BaseUser, UserInDB
from security import user_schemas

router = APIRouter(
    prefix="/security",
    tags=['security'],
    responses={404: {"description": "sec-router not found"}},
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[AsyncSession, Depends(get_session)]):
    # без await возвращаемое значение всегда Coroutine
    user = await depend.authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = depend.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/me", response_model=UserInDB)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    current_user.hashed_password=''
    return current_user


@router.post("/user/registrate")
async def register_new_user(user: user_schemas.CreateUser, session: Annotated[AsyncSession, Depends(get_session)]):
    result = await  user_crud.create_user(user, session)
    return result
