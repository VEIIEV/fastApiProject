from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from security.user_crud import get_user

# tokenUrl,= путь для создания токена,  auto_error=True - если пользователь не авторизован сразу поднимает ошибку
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=True)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_user(token)
    return user
