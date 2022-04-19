import asyncio
import dataclasses
from collections import defaultdict
from typing import Any, AsyncGenerator, Generic, Type, TypeVar

import structlog


@dataclasses.dataclass(frozen=True)
class Event:
    # TODO: event ID
    pass


T = TypeVar("T", bound=Event)


class Subscriber(Generic[T]):
    def __init__(self, queue: asyncio.Queue[T], logger: structlog.BoundLogger):
        self.queue = queue
        self.logger = logger
        self.logger.info("Subscribing to events")

    async def events(self) -> AsyncGenerator[T, None]:
        while True:
            event = await self.queue.get()
            self.queue.task_done()
            self.logger.debug("Consumed event", event_instance=event)
            yield event


class EventManager:
    """
    A simple, in-memory pub/sub application event dispatcher.

    .. note:: This is a toy implementation which assumes a single process.
       For a more production capable event system, see for example broadcaster:
       https://github.com/encode/broadcaster or aioreactive:
       https://github.com/dbrattli/aioreactive
    """

    def __init__(self) -> None:
        # TODO: can we do better than Any here?
        self.queues: dict[Type[Event], set[asyncio.Queue[Any]]] = defaultdict(set)
        self.logger = structlog.get_logger(__name__)

    async def subscribe(self, event_type: Type[T]) -> Subscriber[T]:
        queue: asyncio.Queue[T] = asyncio.Queue()
        self.queues[event_type].add(queue)
        return Subscriber(
            queue, logger=self.logger.bind(event_type=event_type.__name__)
        )

    async def publish(self, event: Event) -> None:
        queues = self.queues[event.__class__]
        self.logger.info(
            "Publishing event", event_instance=event, subscribers_count=len(queues)
        )
        for queue in queues:
            asyncio.create_task(queue.put(event))
