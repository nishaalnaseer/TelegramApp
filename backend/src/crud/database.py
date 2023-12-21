from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager
from os import getenv
from dotenv import load_dotenv


load_dotenv()
db = getenv("database")
host = getenv("database-host")
port = int(getenv("database-port"))
user = getenv("database-username")
password = getenv("database-password")

url = f"mysql+aiomysql://{user}:{password}@{host}:{port}/{db}"
engine = create_async_engine(url,)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)
Base = declarative_base()


@asynccontextmanager
async def getdb() -> AsyncIterator[AsyncConnection]:
    async with engine.begin() as connection:
        yield connection
