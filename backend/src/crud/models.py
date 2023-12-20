from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Integer, BigInteger, DateTime, TIMESTAMP, Column
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.crud.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    tg_id: Mapped[BigInteger] = mapped_column(
        unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    second_name: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    contacts: Mapped[str] = mapped_column(
        String(12), unique=True, nullable=False
    )
    access_hash: Mapped[str] = mapped_column(
        String(19), unique=True, nullable=False
    )

    def __repr__(self) -> str:
        return (f"User(id={self.id!r}, name={self.username!r}, "
                f"fullname={self.first_name!r})")


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    sender: Mapped[Integer] = Column(Integer, ForeignKey("user.id"))
    receiver: Mapped[Integer] = Column(Integer, ForeignKey("user.id"))
    time_sent: Mapped[DateTime] = mapped_column(
        default=TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False
    )


class OTP(Base):
    __tablename__ = "otp"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    receiver: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    time_sent: Mapped[DateTime] = mapped_column(
        default=TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False
    )
