from typing import Any

import strawberry
from sqlalchemy import select
from strawberry.types import Info

from models.idea import Idea as IdeaModel
from models.user import User as UserModel

from .types import Context, Idea, User


async def get_ideas(info: Info[Context, Any]) -> list[Idea]:
    session = info.context["session"]
    async with session.begin():
        stmt = select(IdeaModel)
        result = await session.execute(stmt)
        return [Idea.from_model(idea) for idea in result.scalars().all()]


async def get_users(info: Info[Context, Any], name: str | None = None) -> list[User]:
    session = info.context["session"]
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
