from fastapi import APIRouter, HTTPException
from typing import Any

from app import crud
from app.core.models import (
    UserPublic, UserCreate,
    UserUpdateData, UserUpdatePassword,
    Message
)
from app.utils import security
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


@router.patch('/me', response_model=UserPublic)
async def update_me(
        session: SessionDep, current_user: CurrentUser,
        user_data: UserUpdateData
):
    db_user = await crud.get_user_by_username(
        session=session, username=user_data.username
    )
    if db_user:
        raise HTTPException(403, 'Username already exist')

    user_data = user_data.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.patch('/me/password', response_model=Message)
async def update_password(
        session: SessionDep, current_user: CurrentUser,
        form: UserUpdatePassword
):
    if not security.verify_password(
            form.password, current_user.hashed_password
    ):
        raise HTTPException(403, 'Incorrect password')
    hashed_password = security.get_password_hash(form.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    await session.commit()
    return Message(message='You\'r password was update!')