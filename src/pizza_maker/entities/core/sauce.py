from dataclasses import dataclass
from enum import Enum, auto

from pizza_maker.entities.quantities.milliliters import Milliliters


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


@dataclass(kw_only=True, frozen=True, slots=True)
class Sauce:
    name: SauceName
    milliliters: Milliliters
