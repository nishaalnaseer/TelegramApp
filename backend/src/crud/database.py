from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import asynccontextmanager
from os import getenv

db = getenv("database")
host = getenv("database-host")
port = getenv("database-port")
user = getenv("database-username")
password = getenv("database-password")

url = f"mysql+aiomysql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(url, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = DeclarativeBase()


@asynccontextmanager
async def getdb():
    async with async_session() as session:
        async with session.begin():
            yield session
