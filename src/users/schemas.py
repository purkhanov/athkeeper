from pydantic import BaseModel, EmailStr


class UpdateUserSchema(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    mexc_api_key: str | None = None
    mexc_secret_key: str | None = None


class UserResSchema(BaseModel):
    id: int
    email: str
    telegram_id: int | None
    phone_number: str | None
    first_name: str | None
    last_name: str | None

    is_staff: bool
    is_superuser: bool
    for_free: bool
    ban: bool

    mexc_api_key: str | None
    mexc_secret_key: str | None


class CurrentUserShema(BaseModel):
    id: int
    is_staff: bool
    is_superuser: bool
