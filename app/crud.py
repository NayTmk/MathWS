from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession


from app.core.models import User, UserCreate, UserPublic, GameSession, GameSessionPublic
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
    db_user = await get_user_by_username(
        session=session, username=username
    )
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

async def get_leader_bord(session: AsyncSession):
    leader_bord = []
    statement = (
        select(GameSession)
        .options(selectinload(GameSession.user))
        .order_by(GameSession.score.desc())
        .limit(100)
    )
    result = await session.exec(statement)
    game_sessions = result.all()
    for game_session in game_sessions:
        leader_bord.append(GameSessionPublic(
            score=game_session.score,
            session_date=game_session.session_date,
            username=game_session.user.username
        ))
    return leader_bord

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
        session: AsyncSession, user_id: str, score: int
):
    game_session = GameSession(user_id=user_id, score=score)
    session.add(game_session)
    await session.commit()
    await session.refresh(game_session)
    return game_session