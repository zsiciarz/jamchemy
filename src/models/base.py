from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import config

engine = create_async_engine(
    config.DATABASE_URI,
    echo=True,
    future=True,
)

Base = declarative_base()

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
