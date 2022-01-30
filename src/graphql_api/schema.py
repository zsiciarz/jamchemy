import asyncio
from typing import AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import text

from models.base import engine

fake = Faker()


@strawberry.type
class User:
    name: str
    email: str


async def get_users():
    async with engine.begin() as conn:
        random_id = await conn.scalar(text("select abs(random() % 1000)"))
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
