from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import SiginUpSchema
from ..dependencies import db_dependency
from .services import create_new_user


router = APIRouter(prefix = "/auth", tags = ["auth"])


@router.post("/siginup", status_code = status.HTTP_201_CREATED)
async def siginup(user_request: SiginUpSchema, db: db_dependency):
    user = await create_new_user(user_request, db)
    return {"id": user.id}


# @router.post("/token", status_code = status.HTTP_200_OK, response_model = TokenResponseSchema)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
#     ):
#     pass
