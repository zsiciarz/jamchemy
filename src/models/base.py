from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

engine = create_async_engine(
    "sqlite+aiosqlite:///jamchemy.db",
    echo=True,
    future=True,
)

Base = declarative_base()
