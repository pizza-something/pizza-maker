from abc import ABC, abstractmethod
from dataclasses import dataclass

from pizza_maker.application.ports.event_queue import Event
from pizza_maker.infrastructure.faststream.events import kafka_event_of
from pizza_maker.infrastructure.faststream.publisher_regitry import (
    KafkaPublisherRegistry,
)
from pizza_maker.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)


@dataclass(kw_only=True, slots=True)
class InMemortyEventQueue(TransactionalInMemoryStorage[Event]):
    async def push(self, event: Event) -> None:
        self._storage.append(event)


class KafkaEventQueue(ABC):
    publisher_regitry: KafkaPublisherRegistry

    @abstractmethod
    async def push(self, event: Event) -> None:
        publisher = self.publisher_regitry.publisher_of(type(event))
        await publisher.publish(kafka_event_of(event))
