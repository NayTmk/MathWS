import random

from fastapi import APIRouter, WebSocket, Request
from app.config import settings
from app.utils.game_funcs import generate_tasks


router = APIRouter(prefix='/game', tags=['game'])

connected_clients = {}


@router.websocket('/ws/{room_id}')
async def game(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in connected_clients:
        connected_clients[room_id] = {'websocket': websocket, 'answer': None}
        print(connected_clients)

    try:
        while True:
            client = connected_clients[room_id]
            example, answer = generate_tasks('all_operations', 3)
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
async def get(request: Request):
    room_id = str(random.randint(100, 999))
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='game.html',
        context={'request': request, 'room_id': room_id}
    )