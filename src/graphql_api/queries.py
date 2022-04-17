from typing import Any

import strawberry
from strawberry.types import Info

from models.base import transaction

from .types import Context, Idea, User


async def get_ideas(info: Info[Context, Any]) -> list[Idea]:
    session = info.context["session"]
    idea_repo = info.context["idea_repo"]
    async with transaction(session):
        return [Idea.from_model(idea) async for idea in idea_repo.list()]


async def get_users(info: Info[Context, Any], name: str | None = None) -> list[User]:
    session = info.context["session"]
    user_repo = info.context["user_repo"]
    async with transaction(session):
        return [User.from_model(u) async for u in user_repo.list(name)]


@strawberry.type
class Query:
    ideas: list[Idea] = strawberry.field(resolver=get_ideas)
    users: list[User] = strawberry.field(resolver=get_users)
