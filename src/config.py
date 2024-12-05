import logging
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Mode(Enum):
    prod = 'prod'
    dev = 'dev'


SITE_URL = 'https://athkeeper.com'
MEXC_BASE_URL = 'https://api.mexc.com'

BASE_DIR = Path(__file__).resolve().parent


class Base(BaseSettings):
    BOT_TOKEN: str
    MODE: Mode = Field(default = Mode.dev)

    model_config = SettingsConfigDict(env_file = BASE_DIR / '.env')


class CORSSettings(Base):
    ALLOW_METHODS: list[str] = ['GET', 'POST', 'PATCH', 'DELETE']
    ALLOW_HEADERS: list[str] = ['*']

    @property
    def ORIGINS(self) -> list[str]:
        return [SITE_URL] if self.MODE == Mode.prod else ['*']


class DBSettings(Base):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ECHO(self) -> bool:
        return self.MODE != Mode.prod

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


def configure_logging(level = logging.INFO):
    logging.basicConfig(
        level = level,
        datefmt = "%Y-5m-%d %H:%M:%S",
        format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    )


class Settings(Base):
    cors: CORSSettings = CORSSettings()
    db: DBSettings = DBSettings()


settings = Settings()
