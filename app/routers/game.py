from fastapi import APIRouter, WebSocket, Request, Query, HTTPException
from app.config import settings
from app.utils.game_funcs import generate_tasks
from app.utils.deps import CurrentUser


router = APIRouter(prefix='/game', tags=['game'])

connected_clients = {}


@router.websocket('/ws/{room_id}')
async def game(websocket: WebSocket, room_id: str):
    if user.username != room_id:
        return HTTPException(403, 'This isn\'t your room')
    await websocket.accept()
    print(room_id)
    mode = websocket.query_params.get('mode', 'add')

    if room_id not in connected_clients:
        connected_clients[room_id] = {'websocket': websocket, 'answer': None}

    try:
        while True:
            client = connected_clients[room_id]
            example, answer = generate_tasks(mode, 3)
            data = await websocket.receive_text()
            if client['answer'] == None:
                await websocket.send_text(f'{example} = ?')
            elif str(client['answer']) == data:
                await websocket.send_text(
                    f'Вірно! Наступний приклад \n {example}'
                )
            else:
                await websocket.send_text(
                    f'Не правильно! Наступний приклад \n {example}'
                )
            client['answer'] = answer

    except:
        del connected_clients[room_id]


@router.get("/")
async def get(
        request: Request, user: CurrentUser,
        mode: str = Query('add'),
):
    room_id = user.username
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='game.html',
        context={'request': request, 'room_id': room_id, 'mode': mode}
    )