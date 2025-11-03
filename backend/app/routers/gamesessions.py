from fastapi import APIRouter

from app import crud
from app.core.models import GameSessionPublic, UserLeaderBoard
from app.utils.deps import SessionDep, CurrentUser

router = APIRouter(prefix='/api/game', tags=['game'])

@router.get('/user-game-list', response_model=list[GameSessionPublic])
async def game_session_list(session: SessionDep, user: CurrentUser):
    game_sessions = await crud.get_user_game_list(
        session=session, user_id=user.id
    )
    return game_sessions

@router.get('/last-game-session', response_model=GameSessionPublic)
async def last_game_session(session: SessionDep, user: CurrentUser):
    last_game = await crud.get_last_user_game_session(
        session=session, user_id=user.id
    )
    return last_game

@router.get('/leader-board', response_model=list[UserLeaderBoard])
async def leader_board(session: SessionDep):
    leader_bord = await crud.get_leader_board(session=session)
    return leader_bord