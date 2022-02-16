from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.base import Session
from models.user import User as UserModel

fake = Faker()


@strawberry.type
class User:
    # TODO: expose ID
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
            return [User.from_model(u) for u in result.scalars().all()]


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=get_users)


@strawberry.type
class CreateUserSuccess:
    user: User


@strawberry.type
class CreateUserError:
    cause: str


CreateUserResult = strawberry.union(
    "CreateUserResult",
    (CreateUserSuccess, CreateUserError),
)


@strawberry.type
class Mutation:
    # TODO: use https://strawberry.rocks/docs/guides/tools#merge_types to merge
    # different groups of mutations
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> CreateUserResult:
        try:
            async with Session() as session:
                async with session.begin():
                    user = UserModel(name=name, email=email)
                    session.add(user)
                    return CreateUserSuccess(user=User.from_model(user))
        except IntegrityError:
            return CreateUserError(cause="Email already exists")


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        while True:
            await asyncio.sleep(1)
            yield User(name=fake.name(), email=fake.email())


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
