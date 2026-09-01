import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.database import Base, get_session
from app.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    (
        "postgresql+asyncpg://"
        "reservation:reservation"
        "@localhost:5433/"
        "reservation_salles_test"
    ),
)


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)


test_session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session() -> AsyncGenerator[AsyncSession]:
    async with test_session_factory() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.drop_all,
        )

        await connection.run_sync(
            Base.metadata.create_all,
        )

    yield


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(
        app=app,
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
