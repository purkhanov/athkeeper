from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from .database.base import get_db
from .utils.jwt import decode_jwt
from .users.schemas import CurrentUserShema


oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "/auth/token")

db_dependency = Annotated[AsyncSession, Depends(get_db)]


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"Authenticate": "bearer"},
    )

    try:
        payload = decode_jwt(token)

        user_id = payload.get("id")
        is_staff = payload.get("is_staff")
        is_superuser = payload.get("is_superuser")

        if not user_id:
            raise credentials_exception
        
        return CurrentUserShema(
            id = user_id,
            is_staff = is_staff,
            is_superuser = is_superuser,
        )
    
    except JWTError:
        raise credentials_exception
    

user_dependency = Annotated[CurrentUserShema, Depends(get_current_user)]
