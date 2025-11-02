import pytest
from backend.tests.conftest import override_get_session, auth_token

from backend.app.main import app
from backend.app.core.db import get_session


app.dependency_overrides[get_session] = override_get_session

@pytest.mark.asyncio
async def test_register_user_post_200_and_userdata(client):
    response = await client.post(
        '/api/user/sign-up',
        json={'username': 'qwert', 'password': 'qwerty'}
    )
    assert response.status_code == 200
    assert response.json()['username'] == 'qwert'

@pytest.mark.asyncio
async def test_read_me_get_200_and_user_data(client, auth_token):
    response = await client.get('api/user/me')
    assert response.status_code == 200
    assert response.json()['username'] == 'mark'

@pytest.mark.asyncio
async def test_read_me_patch_200_and_user_data(client, auth_token):
    response = await client.patch(
        '/api/user/me', json={'username': 'qazwsx'}
    )
    assert response.status_code == 200
    assert response.json()['username'] == 'qazwsx'

@pytest.mark.asyncio
async def test_me_password_200(client, auth_token):
    response = await client.patch(
        '/api/user/me/password', json={
            'password': 'qwerty', 'new_password': 'zxcvb'
        }
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'You\'r password was update!'