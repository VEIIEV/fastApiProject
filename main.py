from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import init_db, get_session
from security import security_router
from security.depend import oauth2_scheme, get_current_user
from security.user_crud import get_user_by_id
from security.user_schemas import UserInDB

app = FastAPI()

app.include_router(security_router.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/my/salary")
async def check_my_salary(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """
    return  current authorize user salary
    """

    return {"salary": current_user.salary}


@app.get("/my/next_promotion")
async def check_my_promotion(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """
    return  current authorize user promotion perspective
    """
    return {"promotion date": current_user.next_promotion}


@app.get("/my/data")
async def check_salary_promotion(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """
    return data about current authorize user
    """
    return {"promotion date": current_user.next_promotion,
            "salary": current_user.salary}
