import asyncio

import strawberry
from faker import Faker

fake = Faker()


@strawberry.type
class User:
    name: str
    email: str


async def get_users():
    await asyncio.sleep(1.337)
    return [User(name=fake.name(), email=fake.email())]


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=get_users)


schema = strawberry.Schema(query=Query)
