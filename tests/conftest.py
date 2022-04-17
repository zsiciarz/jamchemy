import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import create_autospec

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from graphql_api.types import Context
from models.base import Base, Session, engine
from models.idea import IdeaRepository
from models.user import UserRepository


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_setup(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(db_setup: None) -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        async with session.begin():
            await IdeaRepository(session).clear()
            await UserRepository(session).clear()
        yield session


@pytest_asyncio.fixture
async def queue() -> AsyncGenerator[asyncio.Queue[int], None]:
    yield asyncio.Queue()


@pytest.fixture
def execution_context(session: AsyncSession, queue: asyncio.Queue[int]) -> Context:
    request = create_autospec(Request)
    return Context(
        request=request,
        response=None,
        queue=queue,
        session=session,
        idea_repo=IdeaRepository(session),
        user_repo=UserRepository(session),
    )
