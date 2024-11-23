from ..database.repository import SQLAlchemyRepository
from ..database.models import User


class AuthRepository(SQLAlchemyRepository):
    model = User
