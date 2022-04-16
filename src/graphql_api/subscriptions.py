from __future__ import annotations

from typing import Any, AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import select
from strawberry.types import Info

from models.user import User as UserModel

from .types import Context, User

fake = Faker()


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(
        self, info: Info[Context, Any]
    ) -> AsyncGenerator[User, None]:
        queue = info.context["queue"]
        session = info.context["session"]
        while True:
            user_id = await queue.get()
            async with session.begin():
                stmt = select(UserModel).where(UserModel.id == user_id)
                result = await session.scalars(stmt)
                user = result.first()
            queue.task_done()
            yield User.from_model(user)
