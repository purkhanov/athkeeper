from sqlalchemy import select
from sqlalchemy.engine import Result
from ..database.repository import SQLAlchemyRepository
from ..database.models import User


class AuthRepository(SQLAlchemyRepository):
    model = User


    async def find_by_email(self, email: str):
        stmt = select(self.model).where(self.model.email == email)
        res: Result = await self.session.execute(stmt)
        return res.scalar_one_or_none()
