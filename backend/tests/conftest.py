import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.core.config import settings
from backend.app.main import app


DATA_BASE_URL = settings.TEST_DATA_BASE_URL
engine = create_async_engine(DATA_BASE_URL, future=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport, base_url='http://test'
    ) as client:
        yield client

@pytest_asyncio.fixture
async def auth_token(client):
    sign_up_payload = {'username': 'mark', 'password': 'qwerty'}
    await client.post('/api/user/sign-up', json=sign_up_payload)
    login_response = await client.post(
        '/login/access-token', data=sign_up_payload,
    )
    jwt_token = login_response.json()['access_token']
    return {'Authorization': f'Bearer {jwt_token}'}