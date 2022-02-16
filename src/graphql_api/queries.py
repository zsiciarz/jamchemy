import strawberry
from sqlalchemy import select

from models.base import Session
from models.idea import Idea as IdeaModel
from models.user import User as UserModel

from .types import Idea, User


async def get_ideas() -> list[Idea]:
    async with Session() as session:
        async with session.begin():
            stmt = select(IdeaModel)
            result = await session.execute(stmt)
            return [Idea.from_model(idea) for idea in result.scalars().all()]


async def get_users(name: str | None = None) -> list[User]:
    async with Session() as session:
        async with session.begin():
            stmt = select(UserModel)
            if name:
                stmt = stmt.filter(UserModel.name.ilike(f"%{name}%"))
            result = await session.execute(stmt)
            return [User.from_model(u) for u in result.scalars().all()]


@strawberry.type
class Query:
    ideas: list[Idea] = strawberry.field(resolver=get_ideas)
    users: list[User] = strawberry.field(resolver=get_users)
