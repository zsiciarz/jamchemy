import strawberry

from models.base import transaction

from .types import ExecutionInfo, Idea, User


async def get_ideas(info: ExecutionInfo) -> list[Idea]:
    idea_repo = info.context.idea_repo
    async with transaction(info.context.session):
        return [Idea.from_model(idea) async for idea in idea_repo.list()]


async def get_users(info: ExecutionInfo, name: str | None = None) -> list[User]:
    user_repo = info.context.user_repo
    async with transaction(info.context.session):
        return [User.from_model(u) async for u in user_repo.list(name)]


@strawberry.type
class Query:
    ideas: list[Idea] = strawberry.field(resolver=get_ideas)
    users: list[User] = strawberry.field(resolver=get_users)
