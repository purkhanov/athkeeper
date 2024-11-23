import logging
from fastapi import APIRouter, HTTPException, status
from ..dependencies import db_dependency, user_dependency
from .service import UserService
from .schemas import UserResSchema, UpdateUserSchema


logger = logging.getLogger(__name__)

router = APIRouter(prefix = "/users", tags = ["user"])

INTERNAL = HTTPException(
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail = "Internal server error"
)


@router.get("", status_code = status.HTTP_200_OK, response_model = UserResSchema)
async def get_user(user: user_dependency, db: db_dependency):
    try:
        user = await UserService(db).get_user(user.id)
    except Exception as ex:
        logger.error("failed to get user", ex)
        raise INTERNAL

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    return user


@router.patch("", status_code = status.HTTP_202_ACCEPTED)
async def update_user(user: user_dependency, user_data: UpdateUserSchema, db: db_dependency):
    try:
        await UserService(db).update_user(user.id, user_data)
    except Exception as ex:
        logger.error("failed to get user", ex)
        raise INTERNAL


@router.delete("", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency):
    try:
        await UserService(db).delete_user()
    except Exception as ex:
        logger.error("failed to delete user", ex)
        raise INTERNAL

