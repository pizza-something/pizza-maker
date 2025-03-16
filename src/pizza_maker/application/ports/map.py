from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from pizza_maker.entities.framework.effect import Effect


class MapTo[StoragesT: Sequence[Any], EffectT: Effect](ABC):
    @abstractmethod
    async def __call__(self, storages: StoragesT, effect: EffectT) -> None: ...
