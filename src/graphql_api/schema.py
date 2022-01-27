import asyncio

import strawberry


@strawberry.type
class User:
    name: str
    email: str


me = User(name="Zbigniew", email="zbigniew@example.com")


async def get_users():
    await asyncio.sleep(1.337)
    return [me]


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=get_users)


schema = strawberry.Schema(query=Query)
