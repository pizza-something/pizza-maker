from faststream.types import SendableMessage

from pizza_maker.application.ports.event_queue import Event, PizzaCreatedEvent
from pizza_maker.infrastructure.pydantic.schemas.output import OutputPizzaSchema


class UnhandledEventError(Exception): ...


def kafka_event_of(event: Event) -> SendableMessage:
    if isinstance(event, PizzaCreatedEvent):
        return OutputPizzaSchema.of(event.pizza)

    raise UnhandledEventError(event)
