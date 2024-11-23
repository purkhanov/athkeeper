import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schemas import SiginUpSchema
from .repository import AuthRepository


logger = logging.getLogger(__name__)


async def create_new_user(user_data: SiginUpSchema, db_session: AsyncSession):
    try:
        return await AuthRepository(db_session).create(user_data.model_dump(exclude_none = True))
    except IntegrityError as e:
        logger.info(f"IntegrityError caught: {e}")

        if "duplicate key value violates unique constraint" in str(e.orig):
            logger.info("User already exists")

            raise HTTPException(
                detail = f"Пользователь с email {user_data.email} уже существует.",
                status_code = status.HTTP_400_BAD_REQUEST,
            )
        
        else:
            logger.exception("Database error")
            raise
        

