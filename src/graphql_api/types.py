from __future__ import annotations

import asyncio
import dataclasses
from typing import Any, TypeAlias

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.types import Info

from models.idea import Idea as IdeaModel
from models.idea import IdeaRepository
from models.user import User as UserModel
from models.user import UserRepository


@dataclasses.dataclass
class Context:
    request: Request | WebSocket
    response: Response | None
    queue: asyncio.Queue[int]
    session: AsyncSession
    idea_repo: IdeaRepository
    user_repo: UserRepository


ExecutionInfo: TypeAlias = Info[Context, Any]


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
