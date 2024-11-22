import logging
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Mode(Enum):
    prod = 'prod'
    dev = 'dev'
    test = 'test'


MODE = Mode.dev
MEXC_BASE_URL = 'https://api.mexc.com'
BASE_DIR = Path(__file__).resolve().parent

if MODE == Mode.prod:
    ORIGINS = ["https://athkeeper.com"]
else:
    ORIGINS = ['*']


class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file = BASE_DIR / '.env')


class DBSettings(Base):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    if MODE == Mode.dev:
        ECHO: bool = True
    else:
        ECHO: bool = False

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class AuthJWT(Base):
    private_key: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    ALGORITHM: str = 'RS256'


def configure_logging(level = logging.INFO):
    logging.basicConfig(
        level = level,
        datefmt = "%Y-5m-%d %H:%M:%S",
        format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )


class Settings(Base):
    auth_jwt: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()


settings = Settings()
