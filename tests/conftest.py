import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base, Session, engine


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_setup(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator[None, None]:
    # TODO: use separate database to run tests against!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(db_setup: None) -> AsyncGenerator[AsyncSession, None]:
    # TODO: clear database or roll back transaction between tests
    async with Session() as session:
        yield session
