from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud
from .schemas import User, UserCreate
from models import db_helper

router = APIRouter()

@router.get("/", response_model=list[User])
async def get_users(
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_users(session=session)

@router.post("/",response_model=User)
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}",response_model=User)
async def get_users(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)):
    user = await crud.get_user(user_id=user_id, session=session)
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={user_id} not found!")