from jose import jwt
from ..config import settings


algorithm = settings.auth_jwt.ALGORITHM

def encode_jwt(
        payload: dict,
        key: str = settings.auth_jwt.private_key.read_text(),
        algorithm: str = algorithm
):
    return jwt.encode(claims = payload, key = key, algorithm = algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key.read_text(),
        algorithm: str = algorithm
):
    return jwt.decode(jwt = token, key = public_key, algorithms = algorithm)
