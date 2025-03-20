from dataclasses import dataclass
from enum import Enum, auto
from typing import overload
from uuid import UUID, uuid4

from pizza_maker.entities.common.effect import Dirty, New, dirty, new
from pizza_maker.entities.common.identified import Identified
from pizza_maker.entities.units.milliliters import Milliliters


class SauceName(Enum):
    tomato_sauce = auto()
    marinara_sauce = auto()
    pesto_sauce = auto()
    alfredo_sauce = auto()
    bbq_sauce = auto()
    garlic_sauce = auto()
    truffle_oil = auto()
    salsa = auto()
    mayo = auto()
    ketchup = auto()


@dataclass(kw_only=True, frozen=True)
class Sauce(Identified[UUID]):
    id: UUID
    pizza_id: UUID
    name: SauceName
    milliliters: Milliliters


@dataclass(kw_only=True, frozen=True)
class SauceData:
    name: SauceName
    milliliters: Milliliters


@overload
def new_sauce_when(
    *, sauce: Sauce, sauce_data: SauceData, pizza_id: UUID,
) -> Dirty[Sauce]: ...


@overload
def new_sauce_when(
    *, sauce: None, sauce_data: SauceData, pizza_id: UUID,
) -> New[Sauce]: ...


def new_sauce_when(
    *, sauce: Sauce | None, sauce_data: SauceData, pizza_id: UUID,
) -> New[Sauce] | Dirty[Sauce]:
    if sauce is None:
        return new(Sauce(
            id=uuid4(),
            name=sauce_data.name,
            milliliters=sauce_data.milliliters,
            pizza_id=pizza_id,
        ))

    return dirty(Sauce(
        id=sauce.id,
        name=sauce_data.name,
        milliliters=sauce_data.milliliters,
        pizza_id=pizza_id,
    ))
