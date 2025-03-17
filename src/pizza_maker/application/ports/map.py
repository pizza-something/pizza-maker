from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from pizza_maker.entities.common.effect import AnyEffect


class MapTo[StoragesT: Sequence[Any], EffectT: AnyEffect](ABC):
    @abstractmethod
    async def __call__(self, storages: StoragesT, effect: EffectT) -> None: ...
