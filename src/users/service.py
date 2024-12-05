import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import User
from .repositoriy import UserRepository
from .schemas import CreateUserSchema, UpdateUserSchema


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.repos = UserRepository(db_session)


    async def get_user(self, pk: int) -> User | None:
        try:
            return await self.repos.find_one(pk)
        except Exception as ex:
            logger.error("failed to get user", ex)
            raise


    async def create_user(self, user_data: CreateUserSchema):
        user_data = user_data.model_dump(exclude_none=True)
        try:
            await self.repos.create(user_data)
        except Exception as ex:
            logger.error('failed to create user', ex)
            raise


    async def update_user(self, pk: int, data: UpdateUserSchema):
        try:
            await self.repos.update(pk, data.model_dump(exclude_none = True))
        except Exception as ex:
            logger.error("failed to update user", ex)
            raise


    async def delete_user(self, pk: int):
        try:
            await self.repos.delete(pk)
        except Exception as ex:
            logger.error("failed to update user", ex)
            raise
