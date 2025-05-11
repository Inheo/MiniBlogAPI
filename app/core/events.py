from typing import Callable, Awaitable, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from .event_types import EventType
from .event_payloads import EventBase

T = TypeVar("T", bound=EventBase)
EventHandler = Callable[[T, AsyncSession], Awaitable[None]]

handlers: dict[EventType, list[EventHandler]] = {}


def on(event_name: EventType):
    def wrapper(fn):
        handlers[event_name].append(fn)
        return fn
    return wrapper


async def emit(event_name: EventType, payload: T, session: AsyncSession):
    for fn in handlers.get(event_name, []):
        await fn(payload, session)