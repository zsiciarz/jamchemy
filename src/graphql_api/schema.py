from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import select

from models.base import Session
from models.user import User as UserModel

fake = Faker()


@strawberry.type
class User:
    name: str | None
    email: str

    @classmethod
    def from_model(cls, model: UserModel) -> User:
        return cls(name=model.name, email=model.email)


async def get_users() -> list[User]:
    async with Session() as session:
        async with session.begin():
            stmt = select(UserModel)  # no filtering... yet
            result = await session.execute(stmt)
            return result.scalars().all()


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=get_users)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        while True:
            await asyncio.sleep(1)
            yield User(name=fake.name(), email=fake.email())


schema = strawberry.Schema(query=Query, subscription=Subscription)
