from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.common.identified import Identified


@dataclass(kw_only=True, frozen=True, slots=True)
class Account(Identified[UUID]):
    id: UUID
