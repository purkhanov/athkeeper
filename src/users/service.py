import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import User
from .repositoriy import UserRepository
from .schemas import UpdateUserSchema


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.repos = UserRepository(db_session)

    
    async def get_user(self, pk: int) -> User:
        return await self.repos.find_one(pk)
    

    async def update_user(self, pk: int, data: UpdateUserSchema):
        await self.repos.update(pk, data.model_dump(exclude_none = True))


    async def delete_user(self, pk: int):
        await self.repos.delete(pk)
