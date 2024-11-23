import logging
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schemas import SiginUpSchema, bcrypt_context
from .repository import AuthRepository
from ..utils.jwt import encode_jwt


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


async def authenticate_user(email: str, password: str, db_session: AsyncSession):
    user = await AuthRepository(db_session).find_by_email(email)

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False
    
    return user


async def create_token(email: str, password: str, db_session: AsyncSession):
    user = await authenticate_user(email, password, db_session)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Не правильный email или пароль.',
            headers = {"Authenticate": "Bearer"}
        )

    expires = datetime.now(timezone.utc) + timedelta(days = 30)

    payload = {
        "id": user.id,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "exp": expires
    }

    return encode_jwt(payload)

