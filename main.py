from typing import Annotated

from fastapi import FastAPI, Depends

from db import init_db
from security import security_router
from security.depend import oauth2_scheme

app = FastAPI()

app.include_router(security_router.router)

@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root(token : Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
