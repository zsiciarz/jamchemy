import contextlib
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import config

engine = create_async_engine(config.DATABASE_URI, future=True)

Base = declarative_base()

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# See: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#migrating-from-the-subtransaction-pattern
@contextlib.asynccontextmanager
async def transaction(session: AsyncSession) -> AsyncGenerator[None, None]:
    if not session.in_transaction():
        async with session.begin():
            yield
    else:
        yield
