from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from pizza_maker.entities.common.effect import LifeCycle
from pizza_maker.entities.core.pizza.pizza import PizzaAggregate
from pizza_maker.entities.core.user import UserAggregate


type AggregateLifeCycle = LifeCycle[UserAggregate | PizzaAggregate]


class MapTo[StoragesT: Sequence[Any]](ABC):
    @abstractmethod
    async def __call__(
        self,
        storages: StoragesT,
        effect: AggregateLifeCycle,
    ) -> None: ...
