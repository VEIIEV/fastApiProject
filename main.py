from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import init_db, get_session
from security import security_router
from security.depend import oauth2_scheme
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


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/get-first-user', response_model=UserInDB)
async def get_first_user(session: Annotated[AsyncSession, Depends(get_session)]):
    first_user = await get_user_by_id(1, session)
    return first_user
