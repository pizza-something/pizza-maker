from abc import ABC, abstractmethod
from collections.abc import Sequence

from pizza_maker.application.ports.private_event_queue import Event


class PublicEventQueue(ABC):
    @abstractmethod
    async def push_batch(self, event_batch: Sequence[Event]) -> None: ...
