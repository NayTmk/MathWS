import jwt

from fastapi import APIRouter, WebSocket, Request, Query
from starlette.websockets import WebSocketDisconnect

from app.config import settings
from app.utils.deps import CurrentUser
from app.domain.game_managers import task_manager, connection_manager
from app.utils.redis import update_score, get_score


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
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get('sub')
    except:
        await websocket.close(
            code=1008, reason='Invalid JWT token'
        )
    if room_id != user_id:
        await websocket.close(
            code=1008, reason='Access denied: not your room"'
        )

    await connection_manager.connect(room_id, websocket)

    try:
        while True:
            client = await connection_manager.get(room_id)
            data = await websocket.receive_text()
            lvl = (await get_score(room_id) + 100) // 100
            example, answer = task_manager.generate_task(mode, lvl)

            if client['answer'] == None:
                msg = f'{example} = ?'
            elif str(client['answer']) == data:
                msg = f'Вірно! Наступний приклад \n {example}'
                await update_score(user_id)
            else:
                msg = f'Не правильно! Наступний приклад \n {example}'

            await connection_manager.send(room_id, msg)
            client['answer'] = answer

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