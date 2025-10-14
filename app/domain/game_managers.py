import asyncio
import operator
import random

from typing import Dict, Any
from starlette.websockets import WebSocket, WebSocketState

from app.utils.redis import set_score, delete_score, get_score, update_score


class GameConnectionManager:
    def __init__(self):
        self.connected_clients: Dict[str, Dict[str, Any]] = {}

    async def connect(
            self, room_id: str, websocket: WebSocket
    ):
        await websocket.accept()
        self.connected_clients[room_id] = {
            'websocket': websocket, 'answer': None
        }
        await set_score(room_id, 0)


    async def disconnect(self, room_id: str):
        client = self.connected_clients.pop(room_id, None)
        if client:
            ws = client['websocket']
            if not ws.client_state == WebSocketState.DISCONNECTED:
                await ws.close()
            await delete_score(room_id)

    async def get(self, room_id:str):
        return self.connected_clients.get(room_id)

    async def send(self, room_id: str, msg: str):
        client = self.connected_clients.get(room_id)
        if client:
            await client['websocket'].send_text(msg)


class GameTaskManager:
    game_mods = {
        'add': {
            'ops': {'+': operator.add},
            'description': 'Додавання'
        },
        'sub': {
            'ops': {'-': operator.sub},
            'description': 'Віднімання'
        },
        'ml': {
            'ops': {'*': operator.mul},
            'description': 'Множення'
        },
        'div': {
            'ops': {'/': operator.floordiv},
            'description': 'Ділення'
        },
        'ad_sub': {
            'ops': {'+': operator.add, '-': operator.sub},
            'description': 'Додавання та віднімання'
        },
        'ml_div': {
            'ops': {'*': operator.mul, '/': operator.floordiv},
            'description': 'Множення та ділення'
        },
        'all_operations': {
            'ops': {'+': operator.add, '-': operator.sub,
                    '*': operator.mul, '/': operator.floordiv},
            'description': 'Всі базові операції'
        }
    }

    def get_random_operator(self, game_mod) -> str:
        operation = random.choice(list(self.game_mods[game_mod]['ops'].keys()))
        return operation

    def _get_func(self, operation):
        func = self.game_mods['all_operations']['ops'][operation]
        return func

    def generate_task(self, game_mod='add', lvl=1):
        if lvl > 10:
            lvl = 10
        operation = self.get_random_operator(game_mod)
        func = self._get_func(operation)
        a, b = self.generate_numbers(operation, lvl)
        return f'{a} {operation} {b}', func(a, b)

    def get_operators_with_desc(self):
        operations = {}
        for operation, description in self.game_mods.items():
            operations[operation] = description['description']
        return operations

    @staticmethod
    def generate_numbers(operation, lvl):
        max_value = 10 ** lvl
        if operation == '-':
            a = random.randint(4, max_value)
            b = random.randint(1, a)
        elif operation == '/':
            b = random.randint(2, max_value // 2)
            result = random.randint(1, max_value // b)
            a = b * result
        else:
            a = random.randint(4, max_value)
            b = random.randint(1, max_value)
        return a, b


class GameManager:
    def __init__(self, connection_manager, task_manager):
        self.connection_manager = connection_manager
        self.task_manager = task_manager

    async def handle_turn(
            self, room_id: str, mode='add',
            client_answer: str | None = None
    ):
        client = await self.connection_manager.get(room_id)
        lvl = (await get_score(room_id) + 100) // 100
        msg = await self.check_up_answer(
            client_answer, client, room_id
        )
        example, answer = self.task_manager.generate_task(mode, lvl)
        client['answer'] = str(answer)
        return {'msg': msg, 'example': example}

    async def check_up_answer(
            self, client_answer: str | None, client, room_id
    ):
        correct_answer = client['answer']
        if correct_answer is None:
            msg = 'Вітаю!'
        elif client_answer == correct_answer:
            msg = 'Вірно! Наступний приклад:'
            await update_score(room_id)
        else:
            msg = 'Не правильно! Наступний приклад:'
        return msg

    async def get_timer(
            self, room_id: str, duration_time: int, on_timeout
    ):
        await asyncio.sleep(duration_time)
        await on_timeout(room_id)


connection_manager = GameConnectionManager()
task_manager = GameTaskManager()
game_manager = GameManager(connection_manager, task_manager)