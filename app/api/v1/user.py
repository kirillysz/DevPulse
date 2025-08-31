from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncEngine

from core.database import get_db
from schemas.user import UserCreate, UserRead
