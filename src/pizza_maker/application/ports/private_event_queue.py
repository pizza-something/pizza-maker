from abc import ABC, abstractmethod
from collections.abc import Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass

from pizza_maker.entities.core.pizza import Pizza


@dataclass(kw_only=True, frozen=True)
class Event: ...


@dataclass(kw_only=True, frozen=True)
class PizzaCreatedEvent(Event):
    pizza: Pizza


class PrivateEventQueue(ABC):
    @abstractmethod
    async def push(self, event: Event) -> None: ...

    @abstractmethod
    def pull_commitable_batch(
        self
    ) -> AbstractAsyncContextManager[Sequence[Event]]: ...
