from __future__ import annotations

from typing import AsyncGenerator

import strawberry

from models.base import transaction

from .types import ExecutionInfo, User


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self, info: ExecutionInfo) -> AsyncGenerator[User, None]:
        queue = info.context.queue
        session = info.context.session
        user_repo = info.context.user_repo
        while True:
            user_id = await queue.get()
            async with transaction(session):
                user = await user_repo.get(user_id)
                if user is None:
                    # TODO: user has been deleted between emitting and consuming
                    # registered event
                    continue
            queue.task_done()
            yield User.from_model(user)
