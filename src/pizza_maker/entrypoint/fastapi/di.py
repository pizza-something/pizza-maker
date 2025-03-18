from dishka import Provider, Scope, make_async_container, provide

from pizza_maker.entrypoint.common.di import ApplicationProvider
from pizza_maker.presentation.fastapi.app import (
    FastAPIAppCoroutines,
    FastAPIAppRouters,
)
from pizza_maker.presentation.fastapi.routers import all_routers


class FastApiProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers

    @provide
    def provide_coroutines(self) -> FastAPIAppCoroutines:
        return []


container = make_async_container(
    FastApiProvider(),
    ApplicationProvider(),
)
