import asyncio
from typing import Any

import strawberry
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

from models.base import transaction
from models.user import User as UserModel

from .types import Context, User


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
    @strawberry.mutation
    async def create_user(
        self, info: Info[Context, Any], name: str, email: str
    ) -> CreateUserResult:
        try:
            session = info.context["session"]
            async with transaction(session):
                user = UserModel(name=name, email=email)
                session.add(user)
            queue = info.context["queue"]
            asyncio.create_task(queue.put(user.id))
            return CreateUserSuccess(user=User.from_model(user))
        except IntegrityError:
            return CreateUserError(cause="Email already exists")
