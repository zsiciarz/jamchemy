import asyncio

import strawberry
from sqlalchemy.exc import IntegrityError

from models.base import transaction

from .types import ExecutionInfo, User


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
        self, info: ExecutionInfo, name: str, email: str
    ) -> CreateUserResult:
        try:
            user_repo = info.context.user_repo
            async with transaction(info.context.session):
                user = await user_repo.create(name=name, email=email)
            # TODO: encapsulate publishing a "user created" event
            queue = info.context.queue
            asyncio.create_task(queue.put(user.id))
            return CreateUserSuccess(user=User.from_model(user))
        # TODO: this should be a User-related exception
        except IntegrityError:
            return CreateUserError(cause="Email already exists")
