from sqlalchemy import select
from sqlalchemy.engine import Result
from src.database.repository import SQLAlchemyRepository
from src.database.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_by_tg_id(self, telegram_id: int) -> User | None:
        stmt = select(self.model).where(self.model.telegram_id == telegram_id)
        res: Result = await self.session.execute(stmt)
        return res.scalar_one_or_none()
