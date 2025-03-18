from dataclasses import dataclass, field
from typing import Any

from faststream.kafka import KafkaBroker
from faststream.kafka.publisher.asyncapi import AsyncAPIPublisher

from pizza_maker.application.ports.event_queue import Event, PizzaCreatedEvent


@dataclass(kw_only=True, slots=True)
class PublisherRegistry:
    broker: KafkaBroker
    _map: dict[type[Event], AsyncAPIPublisher[Any]] = field(
        init=False, default_factory=dict
    )

    def publisher_of(self, event_type: type[Event]) -> AsyncAPIPublisher[Any]:
        return self._map[event_type]

    def __post_init__(self) -> None:
        self._map[PizzaCreatedEvent] = self.broker.publisher("pizza.created.ok")
