from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .users.router import router as user_router
from .auth.router import router as auth_router
from .config import  ORIGINS


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGINS,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(auth_router)
app.include_router(user_router)
