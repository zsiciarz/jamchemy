from __future__ import annotations

from typing import AsyncGenerator

import strawberry
from faker import Faker
from sqlalchemy import select

from models.user import User as UserModel

from .types import ExecutionInfo, User

fake = Faker()


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self, info: ExecutionInfo) -> AsyncGenerator[User, None]:
        queue = info.context.queue
        session = info.context.session
        while True:
            user_id = await queue.get()
            async with session.begin():
                stmt = select(UserModel).where(UserModel.id == user_id)
                result = await session.scalars(stmt)
                user = result.first()
                if user is None:
                    # TODO: user has been deleted between emitting and consuming
                    # registered event
                    continue
            queue.task_done()
            yield User.from_model(user)
