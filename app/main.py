from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.auth import router as auth_router
from api.v1.user import router as user_router

from core.initial_tables import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)