from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead

