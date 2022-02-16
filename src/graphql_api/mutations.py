import strawberry
from sqlalchemy.exc import IntegrityError

from models.base import Session
from models.user import User as UserModel

from .types import User


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
    async def create_user(self, name: str, email: str) -> CreateUserResult:
        try:
            async with Session() as session:
                async with session.begin():
                    user = UserModel(name=name, email=email)
                    session.add(user)
                    return CreateUserSuccess(user=User.from_model(user))
        except IntegrityError:
            return CreateUserError(cause="Email already exists")
