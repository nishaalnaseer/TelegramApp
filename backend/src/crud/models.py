from datetime import datetime
from sqlalchemy import ForeignKey, Integer, BigInteger, DateTime, \
    TIMESTAMP, Column
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.crud.database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import DATETIME


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    tg_id: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
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
    tg_id: Mapped[BigInteger] = mapped_column(
        String(4096), nullable=False, unique=True
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    sender: Mapped[int] = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
    )
    receiver: Mapped[int] = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
    )
    time_sent: Mapped[DATETIME] = mapped_column(
        DATETIME,
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
    time_sent: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(),
        nullable=False
    )
