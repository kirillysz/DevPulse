from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

from crud.user import UserCRUD
from schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/user", tags=["User"])
user_crud = UserCRUD()

@router.post("/add", response_model=UserRead)
async def add_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserRead:    
    result = await user_crud.create_user(
        db=db,
        user_create=user_data
    )

    return result