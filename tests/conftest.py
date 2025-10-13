import pytest_asyncio
from sqlmodel import SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


DATA_BASE_URL = 'postgresql+asyncpg://nayt:qwerty@localhost:5432/mathproject_test'
engine = create_async_engine(DATA_BASE_URL, future=True)
TestingSessionLocal = sessionmaker(
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