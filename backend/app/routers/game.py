import asyncio

from fastapi import APIRouter, WebSocket, Request, Query
from starlette.websockets import WebSocketDisconnect

from backend.app.core.config import settings
from backend.app.utils.deps import CurrentUser
from backend.app.domain.game_managers import (
    connection_manager, game_manager,
    get_user_id_from_websocket_cookies
)

router = APIRouter(prefix='/game', tags=['game'])

@router.websocket('/ws/{room_id}')
async def game(
        websocket: WebSocket, room_id: str,
):
    mode = websocket.query_params.get('mode', 'add')
    user_id = await get_user_id_from_websocket_cookies(websocket)

    if room_id != user_id:
        await websocket.close(
            code=1008, reason='Access denied: not your room'
        )
        return

    await connection_manager.connect(room_id, websocket)

    asyncio.create_task(
        game_manager.get_timer(room_id, 120, mode, game_manager.finish_game)
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