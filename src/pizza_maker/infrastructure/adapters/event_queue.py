from abc import ABC, abstractmethod
from dataclasses import dataclass

from faststream.kafka import KafkaBroker

from pizza_maker.application.ports.event_queue import Event
from pizza_maker.infrastructure.faststream.events import (
    kafka_event_and_topic_of,
)
from pizza_maker.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)


@dataclass(kw_only=True, slots=True)
class InMemortyEventQueue(TransactionalInMemoryStorage[Event]):
    async def push(self, event: Event) -> None:
        self._storage.append(event)


class KafkaEventQueue(ABC):
    broker: KafkaBroker

    @abstractmethod
    async def push(self, event: Event) -> None:
        await self.broker.publish(*kafka_event_and_topic_of(event))
