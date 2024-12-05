from typing import Annotated
from pydantic import BaseModel, Field


API_KEY = Annotated[str, Field(min_length=15, max_length=150)]


class UpdateUserSchema(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    mexc_api_key: API_KEY | None = None
    mexc_secret_key: API_KEY | None = None


class CreateUserSchema(UpdateUserSchema):
    telegram_id: int


class UserResponseSchema(CreateUserSchema):
    pass
