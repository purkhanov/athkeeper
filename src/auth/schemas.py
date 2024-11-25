from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints, AfterValidator
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

HASHPASS = Annotated[
    str,
    StringConstraints(strip_whitespace = True),
    Field(min_length = 6),
    AfterValidator(lambda passw: bcrypt_context.hash(passw))
]

NAME = Annotated[
    str | None,
    StringConstraints(strip_whitespace = True),
    Field(default = None, min_length = 3, max_length = 50),
]

CREATED_AT = Annotated[datetime | str, AfterValidator(lambda date: date.strftime('%d-%m-%Y'))]


class SiginUpSchema(BaseModel):
    email: EmailStr
    first_name: NAME
    password: HASHPASS


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
