import operator
import random

game_mods = {
    'add': {'+': operator.add},
    'sub': {'-': operator.sub},
    'ml': {'*': operator.mul},
    'div': {'/': operator.floordiv},
    'ad_sub': {
        '+': operator.add,
        '-': operator.sub
    },
    'ml_div': {
        '*': operator.mul,
        '/': operator.floordiv
    },
    'all_operations': {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv
    }
}

def generate_tasks(
        game_mod: str = 'add', lvl: int = 1
):
    if game_mod not in game_mods.keys():
        raise ValueError('Game mode value isn\'t correct')

    op = random.choice(list(game_mods[game_mod].keys()))
    func = game_mods[game_mod][op]
    a = random.randint(1, 10**lvl)
    b = random.randint(1, 10**lvl)
    
    return [f'{a} {op} {b}', func(a, b)]
