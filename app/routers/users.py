from fastapi import APIRouter, HTTPException
from typing import Any

from app import crud
from app.core.models import UserPublic, UserCreate
from app.utils.deps import SessionDep, CurrentUser


router = APIRouter(prefix='/api/user', tags=['user'])


@router.post('/sign-up', response_model=UserPublic)
async def register_user(session: SessionDep, user_data: UserCreate) -> Any:
    user = await crud.get_user_by_username(session, user_data.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this username already exists in the system'
        )
    user_create = UserCreate.model_validate(user_data)
    user = await crud.create_user(session, user_create)
    return user


@router.get('/me', response_model=UserPublic)
async def read_me(current_user: CurrentUser):
    return current_user