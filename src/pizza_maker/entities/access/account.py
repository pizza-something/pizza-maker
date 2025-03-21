from dataclasses import dataclass
from uuid import UUID

from effect import Identified


@dataclass(kw_only=True, frozen=True)
class Account(Identified[UUID]):
    id: UUID
