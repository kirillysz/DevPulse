from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

print(settings.DATABASE_URL)

engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session