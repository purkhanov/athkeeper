from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import SiginUpSchema, TokenResponseSchema
from ..dependencies import db_dependency
from .services import create_new_user, create_token


router = APIRouter(prefix = "/auth", tags = ["auth"])


@router.post("/siginup", status_code = status.HTTP_201_CREATED)
async def siginup(user_request: SiginUpSchema, db: db_dependency):
    user = await create_new_user(user_request, db)
    return {"id": user.id}


@router.post("/token", status_code = status.HTTP_200_OK, response_model = TokenResponseSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    token = await create_token(form_data.username, form_data.password, db)
    return {"token_type": "bearer", "access_token": token}
