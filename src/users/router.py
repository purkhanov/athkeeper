import logging
from fastapi import APIRouter, status
from ..dependencies import db_dependency, user_dependency
from .service import UserService
from .schemas import CreateUserSchema, UpdateUserSchema, UserResponseSchema


logger = logging.getLogger(__name__)
router = APIRouter(prefix = '/users', tags = ['user'])

@router.get('', status_code=status.HTTP_200_OK, response_model=UserResponseSchema|None)
async def get_user(user: user_dependency, db: db_dependency):
    return await UserService(db).get_user(user.telegram_id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUserSchema, db: db_dependency):
    await UserService(db).create_user(user_data)


@router.patch('', status_code=status.HTTP_202_ACCEPTED)
async def update_user(user: user_dependency, user_data: UpdateUserSchema, db: db_dependency):
    await UserService(db).update_user(user.telegram_id, user_data)


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency):
    await UserService(db).delete_user(user.telegram_id)
