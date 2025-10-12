from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import User, UserCreate, UserPublic
from app.utils.security import get_password_hash, verify_password


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={'hashed_password': get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_username(
        session: AsyncSession, username: str
) -> UserPublic | None:
    statement = select(User).where(User.username==username)
    session_user = await session.execute(statement)
    return session_user.scalar_one_or_none()


async def authenticate(
        session: AsyncSession, username: str,
        password: str
):
    db_user = await get_user_by_username(session=session, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user