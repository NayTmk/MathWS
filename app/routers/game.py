import jwt

from fastapi import APIRouter, WebSocket, Request, Query
from jwt import InvalidTokenError
from starlette.websockets import WebSocketDisconnect

from app.config import settings
from app.utils.deps import CurrentUser
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
    if room_id != user_id:
        await websocket.close(
            code=1008, reason='Access denied: not your room'
        )
        return

    await connection_manager.connect(room_id, websocket)

    try:
        while True:
            client_answer = await websocket.receive_text()
            response_dct = await game_manager.handle_turn(
                room_id, mode, client_answer
            )
            msg = f"{response_dct['msg']} {response_dct['example']} = ?"
            await connection_manager.send(room_id, msg)

    except WebSocketDisconnect:
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