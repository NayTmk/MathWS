import uuid

from datetime import datetime
from typing import List

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, min_length=4, max_length=255)
    email: EmailStr | None  = Field(
        default=None, unique=True,
        max_length=255, nullable=True
    )


class UserPublic(SQLModel):
    username: str
    best_score: int | None
    game_list: List['GameSessionPublic']


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    best_score: int | None = Field(default=None)

    game_session: list['GameSession'] = Relationship(
        back_populates='user', cascade_delete=True
    )


class GameSessionBase(SQLModel):
    score: int


class GameSessionPublic(GameSessionBase):
    username: str | None
    session_date: datetime


class GameSession(GameSessionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_date: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    user_id: uuid.UUID = Field(foreign_key='user.id')
    user: 'User' = Relationship(back_populates='game_session')


class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(SQLModel):
    sub: str | None = None
