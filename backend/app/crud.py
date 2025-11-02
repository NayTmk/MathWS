from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.core.models import User, UserCreate, UserPublic, GameSession
from backend.app.utils.security import get_password_hash, verify_password


async def create_user(
        session: AsyncSession, user_create: UserCreate
) -> User:
    statement = select(User).where(
        (User.email == user_create.email) | (User.username == user_create.username)
    )
    result = await session.exec(statement)
    existing_user = result.first()
    if existing_user:
        if existing_user.email == user_create.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")

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
    session_user = await session.exec(statement)
    return session_user.first()

async def authenticate(
        session: AsyncSession, username: str,
        password: str
):
    db_user = await get_user_by_username(
        session=session, username=username
    )
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

async def get_leader_board(session: AsyncSession):
    statement = (
        select(User)
        .order_by(User.best_score.desc())
        .limit(100)
    )
    result = await session.exec(statement)
    leader_board = result.all()
    return leader_board

async def get_user_game_list(
        session: AsyncSession, user_id: str
) -> list[GameSession]:
    statement = (
        select(GameSession)
        .where(GameSession.user_id==user_id)
    )
    result = await session.exec(statement)
    user_game_sessions = result.all()
    return user_game_sessions

async def get_last_user_game_session(
        session: AsyncSession, user_id: str
) -> GameSession:
    statement = (
        select(GameSession)
        .where(GameSession.user_id==user_id)
    ).order_by(GameSession.session_date.desc())
    result = await session.exec(statement)
    user_game_session = result.first()
    return user_game_session

async def create_game_session(
        session: AsyncSession, user_id: str, mode: str, score: int
):
    game_session = GameSession(user_id=user_id, mode=mode, score=score)
    session.add(game_session)
    await session.commit()
    await session.refresh(game_session)
    return game_session

async def update_user_best_score(
        session: AsyncSession, user_id, score
):
    statement = (select(User).where(User.id==user_id))
    result = await session.exec(statement)
    user = result.first()
    if (user.best_score or 0) < score:
        user.best_score = score
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user