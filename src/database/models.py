from datetime import datetime
from sqlalchemy import String, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key = True)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now(), default = datetime.now())


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), unique = True, index = True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, index = True)
    phone_number: Mapped[str | None] = mapped_column(String(50))
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))

    is_staff: Mapped[bool] = mapped_column(default = False)
    is_superuser: Mapped[bool] = mapped_column(default = False)
    for_free: Mapped[bool] = mapped_column(default = False)
    ban: Mapped[bool] = mapped_column(default = False)

    mexc_api_key: Mapped[str | None] = mapped_column(String(100))
    mexc_secret_key: Mapped[str | None] = mapped_column(String(150))
