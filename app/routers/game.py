from typing import Dict, Any
import jwt
from fastapi import APIRouter, WebSocket, Request, Query
from app.config import settings
from app.utils.game_funcs import game_manager
from app.utils.deps import CurrentUser


router = APIRouter(prefix='/game', tags=['game'])

connected_clients = {}

class ConnectionManager:
    def __init__(self):
        self.connected_clients: Dict[str, Dict[str, Any]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients[room_id] = {'websocket': websocket, 'answer': None}

    async def disconnect(self, room_id: str):
        client = self.connected_clients.pop(room_id, None)
        if client:
            ws = client['websocket']
            if not ws.client_state.name == 'CLOSE':
                await ws.close()

    async def get(self, room_id:str):
        return self.connected_clients.get(room_id)

    async def send(self, room_id: str, msg: str):
        client = self.connected_clients.get(room_id)
        if client:
            await client['websocket'].send_text(msg)

manager = ConnectionManager()


@router.websocket('/ws/{room_id}')
async def game(
        websocket: WebSocket, room_id: str,
):
    token = websocket.cookies.get('access_token')
    mode = websocket.query_params.get('mode', 'add')

    if token is None:
        await websocket.close(code=1008, reason='JWT token missing')
        return

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get('sub')
    except:
        await websocket.close(code=1008, reason='Invalid JWT token')
        return

    if room_id != user_id:
        await websocket.close(code=1008, reason='Access denied: not your room"')
        return

    await manager.connect(room_id, websocket)


    try:
        while True:
            client = await manager.get(room_id)
            example, answer = game_manager.generate_task(mode, 3)
            data = await websocket.receive_text()

            if client['answer'] == None:
                msg = f'{example} = ?'
            elif str(client['answer']) == data:
                msg = f'Вірно! Наступний приклад \n {example}'
            else:
                msg = f'Не правильно! Наступний приклад \n {example}'

            await manager.send(room_id, msg)
            client['answer'] = answer
    except IsADirectoryError:
        print('discon')
        await manager.disconnect(room_id)


@router.get("/")
async def get(
        request: Request, user: CurrentUser,
        mode: str = Query('add'),
):
    room_id = user.id
    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name='game.html',
        context={'request': request, 'room_id': room_id, 'mode': mode}
    )