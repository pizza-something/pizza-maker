from dataclasses import dataclass
from typing import overload
from uuid import UUID, uuid4

from pizza_maker.entities.common.effect import Dirty, New, dirty, new
from pizza_maker.entities.common.identified import Identified
from pizza_maker.entities.units.millimeters import Millimeters


@dataclass(kw_only=True, frozen=True, slots=True)
class Crust(Identified[UUID]):
    id: UUID
    pizza_id: UUID
    thickness: Millimeters
    diameter: Millimeters


@dataclass(kw_only=True, frozen=True, slots=True)
class CrustData:
    thickness: Millimeters
    diameter: Millimeters


@overload
def new_crust_when(
    *, crust: Crust, crust_data: CrustData, pizza_id: UUID
) -> Dirty[Crust]: ...


@overload
def new_crust_when(
    *, crust: None, crust_data: CrustData, pizza_id: UUID
) -> New[Crust]: ...


def new_crust_when(
    *, crust: Crust | None, crust_data: CrustData, pizza_id: UUID
) -> New[Crust] | Dirty[Crust]:
    if crust is None:
        return new(Crust(
            id=uuid4(),
            thickness=crust_data.thickness,
            diameter=crust_data.diameter,
            pizza_id=pizza_id,
        ))

    return dirty(Crust(
        id=crust.id,
        thickness=crust_data.thickness,
        diameter=crust_data.diameter,
        pizza_id=pizza_id,
    ))
