import strawberry
from sqlalchemy import select

from models.base import Session
from models.user import User as UserModel

from .types import User


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
    users: list[User] = strawberry.field(resolver=get_users)
