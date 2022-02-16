from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import strawberry
from faker import Faker

from .types import User

fake = Faker()


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        i = 10000
        while True:
            await asyncio.sleep(1)
            yield User(
                id=strawberry.ID(f"User:{i}"), name=fake.name(), email=fake.email()
            )
            i += 1
