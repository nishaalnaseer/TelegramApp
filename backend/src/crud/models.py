from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, \
    TIMESTAMP, Column
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.crud.database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import DATETIME, BIGINT, INTEGER


class User(Base):
    __tablename__ = "user"
    id: Mapped[BIGINT] = mapped_column(
        BIGINT(unsigned=True), unique=True, nullable=False,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=True
    )
    first_name: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(30), nullable=True
    )
    phone: Mapped[str] = mapped_column(
        String(12), unique=True, nullable=True
    )

    def __repr__(self) -> str:
        return (f"User(id={self.id!r}, name={self.username!r}, "
                f"fullname={self.first_name!r})")


class Message(Base):
    __tablename__ = "message"
    id: Mapped[BIGINT] = mapped_column(
        BIGINT(unsigned=True), nullable=False, unique=True,
        primary_key=True
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    sender: Mapped[BIGINT] = Column(
        BIGINT(unsigned=True),
        ForeignKey("user.id"),
        nullable=False,
    )
    receiver: Mapped[BIGINT] = Column(
        BIGINT(unsigned=True),
        ForeignKey("user.id"),
        nullable=False,
    )
    time_sent: Mapped[DATETIME] = mapped_column(
        DATETIME,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        nullable=False
    )


class OTP(Base):
    __tablename__ = "otp"
    id: Mapped[INTEGER] = mapped_column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)

    # contact number of the user, not mapped as it may be private
    receiver: Mapped[str] = mapped_column(
        String(12),
        nullable=False
    )

    time_sent: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(),
        nullable=False
    )


class MyMessage(Base):
    __tablename__ = "my_message"
    id: Mapped[BIGINT] = mapped_column(
        BIGINT(unsigned=True), nullable=False, unique=True,
        primary_key=True
    )
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    sender: Mapped[BIGINT] = Column(
        BIGINT(unsigned=True),
        ForeignKey("user.id"),
        nullable=False,
    )
    receiver: Mapped[BIGINT] = Column(
        BIGINT(unsigned=True),
        ForeignKey("user.id"),
        nullable=False,
    )
    time_sent: Mapped[DATETIME] = mapped_column(
        DATETIME,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        nullable=False
    )
