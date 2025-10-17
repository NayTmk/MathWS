import pytest
from httpx import AsyncClient, ASGITransport
from tests.conftest import override_get_session, auth_token

from app.main import app
from app.core.db import get_session


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
    response = await client.get('api/user/me', headers=auth_token)
    assert response.status_code == 200
    assert response.json()['username'] == 'mark'

@pytest.mark.asyncio
async def test_read_me_patch_200_and_user_data(client):
    ...