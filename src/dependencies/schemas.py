from pydantic import BaseModel


class CurrentUser(BaseModel):
    telegram_id: int
    username: str | None = None