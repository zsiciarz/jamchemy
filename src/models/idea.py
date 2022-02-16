from sqlalchemy import Column, ForeignKey, Integer, String
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
