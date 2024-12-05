import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .users.router import router as user_router
from src.config import settings


app = FastAPI()
settings.logging.configure_logging(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors.ORIGINS,
    allow_credentials = True,
    allow_methods = settings.cors.ALLOW_METHODS,
    allow_headers = settings.cors.ALLOW_HEADERS,
)

app.include_router(user_router)
