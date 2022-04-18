import asyncio
import dataclasses
import logging
from collections import defaultdict
from typing import Any, AsyncGenerator, Generic, Type, TypeVar

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Event:
    # TODO: event ID
    pass


@dataclasses.dataclass(frozen=True)
class UserCreatedEvent(Event):
    # TODO: move somewhere closer to User domain
    user_id: int


T = TypeVar("T", bound=Event)


class Subscriber(Generic[T]):
    def __init__(self, queue: asyncio.Queue[T]):
        self.queue = queue

    async def events(self) -> AsyncGenerator[T, None]:
        while True:
            event = await self.queue.get()
            self.queue.task_done()
            logger.info(f"Consumed event: {event}")
            yield event


class EventManager:
    def __init__(self) -> None:
        # TODO: can we do better than Any here?
        self.queues: dict[Type[Event], set[asyncio.Queue[Any]]] = defaultdict(set)

    async def subscribe(self, event_type: Type[T]) -> Subscriber[T]:
        logger.info(f"Subscribing to events of type {event_type.__name__!r}")
        queue: asyncio.Queue[T] = asyncio.Queue()
        self.queues[event_type].add(queue)
        return Subscriber(queue)

    async def publish(self, event: Event) -> None:
        queues = self.queues[event.__class__]
        logger.info(f"Publishing event: {event} to {len(queues)} subscribers")
        for queue in queues:
            asyncio.create_task(queue.put(event))
