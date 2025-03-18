from collections.abc import Awaitable, Callable
from typing import Any

from faststream.kafka import KafkaRouter


def default_route_of(
    topic: str
) -> Callable[[Callable[..., Awaitable[Any]]], KafkaRouter]:
    def get_route(hander: Callable[..., Awaitable[Any]]) -> KafkaRouter:
        router = KafkaRouter()
        router.subscriber(
            topic,
            group_id="pizza-maker",
            retry=True,
            auto_commit=False,
            max_workers=16,
        )(hander)

        return router

    return get_route
