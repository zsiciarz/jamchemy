from typing import AsyncGenerator

from sqlalchemy import Column, ForeignKey, Integer, String, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Idea(Base):
    __tablename__ = "idea"

    id: M[int] = Column(Integer, primary_key=True)
    author_id: M[int] = Column(
        Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
    )
    author: M[User] = relationship("User", lazy="joined")
    summary: M[str] = Column(String, unique=True, nullable=False)
    description: M[str | None] = Column(String, nullable=True)


class IdeaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def clear(self) -> None:
        stmt = delete(Idea)
        await self.session.execute(stmt)

    async def list(self) -> AsyncGenerator[Idea, None]:
        stmt = select(Idea)
        result = await self.session.execute(stmt)
        for idea in result.scalars().all():
            yield idea
