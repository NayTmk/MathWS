import operator
import random


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

game_manager = GameTaskManager()