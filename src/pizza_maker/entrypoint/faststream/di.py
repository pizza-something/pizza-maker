from dishka import Provider, Scope, make_async_container, provide
from faststream import FastStream
from faststream.kafka import KafkaBroker

from pizza_maker.entrypoint.common.di import (
    ApplicationProvider,
)
from pizza_maker.presentation.faststream.app import app_with


class FastStreamProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_faststream(self, broker: KafkaBroker) -> FastStream:
        return app_with(broker)


container = make_async_container(
    FastStreamProvider(),
    ApplicationProvider(),
)
