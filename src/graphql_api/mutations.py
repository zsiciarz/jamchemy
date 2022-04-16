from typing import Any

import strawberry
from sqlalchemy.exc import IntegrityError
from strawberry.types import Info

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
            async with session.begin():
                user = UserModel(name=name, email=email)
                session.add(user)
            # TODO: enqueue user created event
            print(f"User {user} created")
            return CreateUserSuccess(user=User.from_model(user))
        except IntegrityError:
            return CreateUserError(cause="Email already exists")
