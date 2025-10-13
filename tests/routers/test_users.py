import pytest
from httpx import AsyncClient, ASGITransport
from app.core.db import get_session
from app.main import app
from tests.conftest import override_get_session


app.dependency_overrides[get_session] = override_get_session

@pytest.mark.asyncio
async def test_register_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport, base_url='http://test'
    ) as client:
        response = await client.post(
            '/user/sign-up',
            json={'username': 'qwert', 'password': 'qwerty'}
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport, base_url='http://test'
    ) as client:
        sing_up_payload = {'username': 'qwerty', 'password': 'qwerty'}
        await client.post(
            '/user/sign-up', json=sing_up_payload
        )
        login_response = await client.post(
            '/login/access-token', data=sing_up_payload
        )
        assert login_response.status_code == 200, login_response.text

        jwt_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {jwt_token}'}

        response = await client.get('/user/me', headers=headers)
        assert response.status_code == 200
        assert response.json()['username'] == 'qwerty'