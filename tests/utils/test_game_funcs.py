import pytest
from app.domain import game_managers


def test_generate_tasks_add_correct(monkeypatch):

    monkeypatch.setattr(
        game_funcs.random,
        'randint',
        lambda a, b: 4
    )

    test_answer, result = game_funcs.generate_tasks('add', 1)

    assert (test_answer, result) == ('4 + 4', 8)


def test_generate_tasks_sub_correct(monkeypatch):
    values = [12, 5]

    def fake_randint(a, b):
        return values.pop(0)

    monkeypatch.setattr(
        game_funcs.random, 'randint', fake_randint
    )

    test_answer, result = game_funcs.generate_tasks('sub', 2)

    assert (test_answer, result) == ('12 - 5', 7)


def test_generate_tasks_all_operations_correct(monkeypatch):
    values = [21, 7]

    def fake_randint(a, b):
        return values.pop(0)

    monkeypatch.setattr(
        game_funcs.random, 'randint', fake_randint
    )

    monkeypatch.setattr(
        game_funcs.random, 'choice', lambda op: '/'
    )

    test_answer, result = game_funcs.generate_tasks(
        'all_operations', 3
    )

    assert (test_answer, result) == ('21 / 7', 3)


def test_generate_tasks_error():
    with pytest.raises(ValueError, match='Game mode value isn\'t correct'):
        test_answer, result = game_funcs.generate_tasks(
            'error_ex', 2
        )