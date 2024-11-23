from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from ..config import settings


engine = create_async_engine(settings.db.DATABASE_URL, echo = settings.db.ECHO)

async_session_maker = async_sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()
        
