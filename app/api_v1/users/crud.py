from typing import List
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from .schemas import UserCreate

async def get_users(session: AsyncSession)-> List[User]:
    stmt = select(User).order_by(User.id.desc())
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)

async def create_user(session: AsyncSession, user_in: UserCreate) -> User | None:
   user = User(**user_in.model_dump())
   session.add(user)
   await session.commit()
   # await session.refresh(user)
   return user