from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlalchemy.ext.asyncio import AsyncSession

from security.depend import get_current_user
from security.user_schemas import BaseUser

router = APIRouter(
    prefix="/security",
    tags=['security'],
    responses={404: {"description": "sec-router not found"}},
)


@router.get("/user/me", response_model=BaseUser)
async def read_users_me(current_user: Annotated[BaseUser, Depends(get_current_user)]):
    return current_user

