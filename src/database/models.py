from datetime import datetime
from enum import Enum
from sqlalchemy import String, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Role(Enum):
    user = 'user'
    admin = 'admin'


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key = True)
    created_at: Mapped[datetime] = mapped_column(
        server_default = func.now(),
        default = datetime.now(),
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, index = True, unique=True)
    username: Mapped[str | None] = mapped_column(index = True)
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))

    role: Mapped[Role] = mapped_column(default=Role.user)
    for_free: Mapped[bool] = mapped_column(default = False)
    ban: Mapped[bool] = mapped_column(default = False)

    mexc_api_key: Mapped[str | None] = mapped_column(String(100))
    mexc_secret_key: Mapped[str | None] = mapped_column(String(150))

    deleted: Mapped[bool] = mapped_column(default = False)
    