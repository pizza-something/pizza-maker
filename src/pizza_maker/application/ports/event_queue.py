from abc import ABC, abstractmethod
from dataclasses import dataclass

from pizza_maker.entities.core.pizza.pizza import Pizza


@dataclass(kw_only=True, frozen=True)
class Event: ...


@dataclass(kw_only=True, frozen=True)
class PizzaCreatedEvent(Event):
    pizza: Pizza


class EventQueue(ABC):
    @abstractmethod
    async def push(self, event: Event) -> None: ...
