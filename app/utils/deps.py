import jwt

from app.db import get_session
from app.utils.security import settings
from app.models import User, TokenPayload

from fastapi import Depends
from typing import Annotated
from jwt import InvalidTokenError
from pydantic import ValidationError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login/access-token')

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep) -> User | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except(InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=400,
            detail='Could not validate credentials'
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]