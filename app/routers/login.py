from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.utils.deps import SessionDep
from app.models import Token
from app.utils import security
from app import crud


router = APIRouter(tags=['login'])

@router.post('/login/access-token')
async def login_access_token(
        session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await crud.authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect user name or password'
        )
    access_token_expire = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_TIME
    )
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expire
        )
    )