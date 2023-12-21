from typing import List

from sqlalchemy import select

from src.crud.database import async_session, engine, Base
from src.crud.models import OTP, User, Message


async def insert_object(obj: OTP | User | Message):
    async with async_session() as session:
        async with session.begin():
            session.add(obj)


async def insert_objects(objects: List[OTP | User | Message]):
    async with async_session() as session:
        async with session.begin():
            await session.add_all(
                objects
            )
            await session.commit()


async def initialise_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_user_by_id(user_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            record = await session.execute(
                select(User).where(User.id == user_id)
            )
            existing_user = record.scalar()

            if existing_user:
                return User(
                    id=existing_user.id,
                    username=existing_user.username,
                    first_name=existing_user.first_name,
                    last_name=existing_user.last_name,
                    phone=existing_user.phone,
                )
            else:
                return None


async def update_user(user: User) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.merge(
                user
            )
            await session.commit()