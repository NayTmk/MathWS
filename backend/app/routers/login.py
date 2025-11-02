from typing import Annotated

from datetime import timedelta
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.config import settings
from backend.app.utils.deps import SessionDep
from backend.app.utils import security
from backend.app import crud


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
    access_token = security.create_access_token(
            user.id, expires_delta=access_token_expire
        )
    response = JSONResponse(
        {'access_token': access_token, 'token_type': 'bearer'}
    )
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        max_age=3600,
        samesite='lax'
    )
    return response