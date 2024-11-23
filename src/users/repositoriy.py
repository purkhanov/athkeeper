from ..database.repository import SQLAlchemyRepository
from ..database.models import User


class UserRepository(SQLAlchemyRepository):
    model = User