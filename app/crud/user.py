from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.user import User
from schemas.user import UserRead, UserCreate

from core.security import hash_password

class UserCRUD:
    @staticmethod
    async def _get_user_by_field(db: AsyncSession, field: str, value) -> UserRead | bool:
        query = select(User).options(selectinload(User.tasks)).where(getattr(User, field) == value)

        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            return UserRead.model_validate(user)
        
        return False

    @staticmethod
    async def get_user_for_auth(db: AsyncSession, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await db.execute(query)

        user = result.scalar_one_or_none()

        if user:
            return user
        
        return None

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: int) -> UserRead:
        return await UserCRUD._get_user_by_field(db, "id", id)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> UserRead:
        return await UserCRUD._get_user_by_field(db, "email", email)

    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> UserRead:
        existing_user = await UserCRUD.get_user_by_email(db, user_create.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        hashed_password = hash_password(user_create.password)
        new_user = User(**user_create.model_dump(exclude={"password"}), password=hashed_password)

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user, ["tasks"])
        
        return UserRead.model_validate(new_user)
