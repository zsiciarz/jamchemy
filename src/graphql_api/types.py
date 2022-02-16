from __future__ import annotations

import strawberry

from models.user import User as UserModel


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
