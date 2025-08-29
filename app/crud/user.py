from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserRead, UserCreate

from app.core.security import hash_password

class UserCRUD:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: int) -> Optional[UserRead]:
        query = select(User).where(User.id == id)

        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            return UserRead.model_validate(user)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserRead]:
        query = select(User).where(User.email == email)

        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            return UserRead.model_validate(user)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> UserRead:
        hashed_password = hash_password(user_create.password)
        new_user = User(**user_create.model_dump(exclude={"password"}), password=hashed_password)

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user)
        
        return UserRead.model_validate(new_user)
