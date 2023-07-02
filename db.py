import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# connection pool - список соеденений с бд


# future – Use the 2.0 style Engine and Connection API.

# echo=False – if True, the Engine will log all statements as well
# as a repr() of their parameter lists to the default log handler,
# which defaults to sys.stdout for output

# Engine= Connects a Pool and Dialect together to provide a source of database connectivity and behavior.
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# asyncpg.create_pool(settings.SQLALCHEMY_DATABASE_URI)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # metadata.create_all не выполняется асинхронно,
        # поэтому мы использовали run_sync для его синхронного выполнения в асинхронной функции.
        await conn.run_sync(Base.metadata.create_all)



# фабрика, которая генерируют новую сессия при каждом вызове
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# используется как зависимости, для создания сессии с бд
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            print(str(type(e)))
