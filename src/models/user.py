from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped as M

from .base import Base


class User(Base):
    __tablename__ = "user"

    id: M[int] = Column(Integer, primary_key=True)
    email: M[str] = Column(String, unique=True, nullable=False)
    name: M[str | None] = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
