from collections.abc import Iterator

from fastapi import APIRouter

from pizza_maker.presentation.fastapi.routes.create_pizza import (
    create_pizza_router,
)
from pizza_maker.presentation.fastapi.routes.healthcheck import (
    healthcheck_router,
)


all_routers = (
    healthcheck_router,
    create_pizza_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
