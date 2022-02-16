from __future__ import annotations

import strawberry

from models.idea import Idea as IdeaModel
from models.user import User as UserModel


@strawberry.type
class Idea:
    id: strawberry.ID
    author: User
    summary: str
    description: str | None

    @classmethod
    def from_model(cls, model: IdeaModel) -> Idea:
        return cls(
            id=strawberry.ID(f"Idea:{model.id}"),
            author=User.from_model(model.author),
            summary=model.summary,
            description=model.description,
        )


@strawberry.type
class User:
    id: strawberry.ID
    name: str | None
    email: str

    @classmethod
    def from_model(cls, model: UserModel) -> User:
        return cls(
            # TODO: global IDs
            id=strawberry.ID(f"User:{model.id}"),
            name=model.name,
            email=model.email,
        )
