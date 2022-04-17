from typing import AsyncGenerator

from sqlalchemy import Column, Integer, String, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped as M

from .base import Base


class User(Base):
    __tablename__ = "user"

    id: M[int] = Column(Integer, primary_key=True)
    email: M[str] = Column(String, unique=True, nullable=False)
    name: M[str | None] = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def clear(self) -> None:
        stmt = delete(User)
        await self.session.execute(stmt)

    async def list(self, name: str | None) -> AsyncGenerator[User, None]:
        stmt = select(User)
        if name:
            stmt = stmt.filter(User.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        for user in result.scalars().all():
            yield user
