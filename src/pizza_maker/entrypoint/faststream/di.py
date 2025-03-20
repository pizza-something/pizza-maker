from dishka import make_async_container

from pizza_maker.entrypoint.common.di import (
    ApplicationProvider,
)


container = make_async_container(ApplicationProvider())
