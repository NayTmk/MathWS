import jwt

from fastapi import Depends, Cookie
from typing import Annotated
from jwt import InvalidTokenError
from pydantic import ValidationError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.core.db import get_session
from backend.app.utils.security import settings
from backend.app.core.models import User, TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login/access-token', auto_error=False)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(
        session: SessionDep, token: TokenDep,
        access_token: str = Cookie(default=None)
) -> User:
    try:
        if access_token:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        else:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        token_data = TokenPayload(**payload)
    except(InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=401,
            detail='You are not authorized'
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]