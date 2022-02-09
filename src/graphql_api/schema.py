import asyncio
from typing import AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import literal_column, select

from models.base import engine

fake = Faker()


@strawberry.type
class User:
    name: str
    email: str


async def get_users() -> list[User]:
    async with engine.begin() as conn:
        stmt = select(literal_column("abs(random()) % 1000").label("id"))
        random_id = await conn.scalar(stmt)
    email = f"user{random_id}@{fake.domain_name()}"
    return [User(name=fake.name(), email=email)]


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
