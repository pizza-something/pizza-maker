from dataclasses import dataclass

from pizza_maker.entities.quantities.millimeters import Millimeters


@dataclass(kw_only=True, frozen=True, slots=True)
class Crust:
    thickness: Millimeters
    diameter: Millimeters
