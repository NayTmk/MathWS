from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession


from app.core.models import User, UserCreate, UserPublic, GameSession
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
    session_user = await session.exec(statement)
    return session_user.first()

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

async def get_leader_bord(session):
    leader_bord = {}
    statement = (
        select(GameSession)
        .options(selectinload(GameSession.user))
        .order_by(GameSession.score.desc())
        .limit(100)
    )
    result = await session.exec(statement)
    game_sessions = result.all()

    for game_session in game_sessions:
        leader_bord[game_session.user.username] = game_session.score

    return leader_bord