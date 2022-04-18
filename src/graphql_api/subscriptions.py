from __future__ import annotations

from typing import AsyncGenerator

import strawberry

from events import UserCreatedEvent
from models.base import transaction

from .types import ExecutionInfo, User


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self, info: ExecutionInfo) -> AsyncGenerator[User, None]:
        event_manager = info.context.event_manager
        session = info.context.session
        user_repo = info.context.user_repo
        subscriber = await event_manager.subscribe(UserCreatedEvent)
        async for event in subscriber.events():
            async with transaction(session):
                user = await user_repo.get(event.user_id)
                if user is None:
                    # TODO: user has been deleted between emitting and consuming
                    # registered event
                    continue
            yield User.from_model(user)
