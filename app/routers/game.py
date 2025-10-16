import asyncio
import jwt

from fastapi import APIRouter, WebSocket, Request, Query
from jwt import InvalidTokenError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.websockets import WebSocketDisconnect

from app import crud
from app.core.config import settings
from app.core.db import engine
from app.utils.deps import CurrentUser
from app.utils.redis import get_score
from app.domain.game_managers import connection_manager, game_manager


router = APIRouter(prefix='/game', tags=['game'])

@router.websocket('/ws/{room_id}')
async def game(
        websocket: WebSocket, room_id: str,
):
    token = websocket.cookies.get('access_token')
    mode = websocket.query_params.get('mode', 'add')

    if not token:
        await websocket.close(
            code=1008, reason='JWT token missing'
        )
        return

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get('sub')
    except InvalidTokenError:
        await websocket.close(
            code=1008, reason='Invalid JWT token'
        )
        return

    if room_id != user_id:
        await websocket.close(
            code=1008, reason='Access denied: not your room'
        )
        return

    await connection_manager.connect(room_id, websocket)

    async def finish_game(room_id):
        score = int(await get_score(room_id) or 0)
        async with AsyncSession(engine) as session:
            await crud.create_game_session(session, room_id, score)
            await crud.update_user_best_score(session, room_id, score)
        await connection_manager.send(room_id, 'Гра завершина!')
        await connection_manager.disconnect(room_id)

    asyncio.create_task(
        game_manager.get_timer(room_id, 120, finish_game)
    )

    try:
        while True:
            client_answer = await websocket.receive_text()
            response_dct = await game_manager.handle_turn(
                room_id, mode, client_answer
            )
            msg = f"{response_dct['msg']} {response_dct['example']} = ?"
            await connection_manager.send(room_id, msg)
    except WebSocketDisconnect:
        print('User was disconnected')
        await connection_manager.disconnect(room_id)


@router.get("/")
async def get(
        request: Request, user: CurrentUser,
        mode: str = Query('add'),
):
    room_id = user.id
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='game.html',
        context={
            'request': request, 'room_id': room_id,
            'mode': mode
        }
    )