import json
import logging
from logging import LogRecord, FileHandler, StreamHandler
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
    MODE: Mode = Field(default = Mode.prod)

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


class JsonFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'module': record.module,
            'line': record.lineno,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)


class LoggingSettings(Base):
    def configure_logging(self, level = logging.INFO) -> None:
        date_format = "%Y-%m-%d %H:%M:%S"
        text_format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"

        logger = logging.getLogger()
        logger.setLevel(level)
        logger.handlers.clear()

        if self.MODE == Mode.prod:
            log_file_path = Path(BASE_DIR.parent / 'logs/logs.log')
            log_file_path.parent.mkdir(parents=True, exist_ok=True) 
            file_handler = FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(JsonFormatter(datefmt=date_format))
            logger.addHandler(file_handler)
        else:
            console_handler = StreamHandler()
            console_handler.setFormatter(logging.Formatter(fmt=text_format, datefmt=date_format))
            logger.addHandler(console_handler)


class Settings(Base):
    logging: LoggingSettings = LoggingSettings()
    cors: CORSSettings = CORSSettings()
    db: DBSettings = DBSettings()


settings = Settings()
