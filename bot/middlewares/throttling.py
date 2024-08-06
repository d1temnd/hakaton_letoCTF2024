from aiogram import BaseMiddleware, Router
from aiogram.types import Message
from aiogram.dispatcher.event.bases import CancelHandler
from typing import Any, Awaitable, Callable, Dict
import asyncio


def rate_limit(limit: float, key: str = None):
    """
    Decorator for configuring rate limit for handlers.
    :param limit: Rate limit in seconds
    :param key: Key for rate limit
    """

    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, default_rate: float = 1.0, key_prefix: str = "antiflood_"):
        self.default_rate = default_rate
        self.prefix = key_prefix
        self.rates = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        handler_name = handler.__name__
        limit = getattr(handler, "throttling_rate_limit", self.default_rate)
        key = getattr(handler, "throttling_key", f"{self.prefix}_{handler_name}")

        try:
            await self.throttle(key, rate=limit)
        except asyncio.TimeoutError:
            raise CancelHandler()

        return await handler(event, data)

    async def throttle(self, key: str, rate: float) -> None:
        if key not in self.rates:
            self.rates[key] = {"last_call": 0, "lock": asyncio.Lock()}

        async with self.rates[key]["lock"]:
            now = asyncio.get_event_loop().time()
            if now - self.rates[key]["last_call"] < rate:
                raise asyncio.TimeoutError()
            self.rates[key]["last_call"] = now


# Usage example:
router = Router()


@router.message()
@rate_limit(5, "example_limit")
async def example_handler(message: Message):
    # Your handler logic here
    pass


# Apply middleware to router
router.message.middleware(ThrottlingMiddleware(default_rate=1))
