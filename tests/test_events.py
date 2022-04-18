import asyncio
import dataclasses

import pytest

from events import Event, EventManager, Subscriber


@dataclasses.dataclass(frozen=True)
class ExampleEvent(Event):
    message: str


@pytest.mark.asyncio
async def test_simple_pubsub() -> None:
    event_manager = EventManager()
    subscriber = await event_manager.subscribe(ExampleEvent)

    async def consume_event(s: Subscriber[ExampleEvent]) -> str:
        event = await anext(s.events())
        return event.message

    example_event = ExampleEvent(message="Hello world")
    producer = asyncio.create_task(event_manager.publish(example_event))
    consumer = asyncio.create_task(consume_event(subscriber))
    _, message = await asyncio.gather(producer, consumer)
    assert message == example_event.message
