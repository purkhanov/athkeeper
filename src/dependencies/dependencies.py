import logging
from typing import Annotated
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.base import get_db
from src.config import settings
from .utils import check_init_data
from .exceptions import DataOutdatedError, InitDataHashMismatch
from .schemas import CurrentUser


logger = logging.getLogger(__name__)
db_dependency = Annotated[AsyncSession, Depends(get_db)]

def get_init_data(request: Request) -> str:
    init_data = request.headers.get("Authorization")

    if not init_data:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authorization header is empty"
        )
    
    return init_data


def get_current_user(request: Request):
    init_data = get_init_data(request)

    try:
        user = check_init_data(init_data, settings.BOT_TOKEN)
    except (DataOutdatedError, InitDataHashMismatch) as ex:
        ex_str = str(ex)
        logger.error(ex_str)
        
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = ex_str
        )
    
    except Exception as ex:
        logger.error(str(ex))
        raise
    
    return CurrentUser(
        telegram_id = user.get("id"),
        username = user.get("username")
    )
    

user_dependency = Annotated[CurrentUser, Depends(get_current_user)]
