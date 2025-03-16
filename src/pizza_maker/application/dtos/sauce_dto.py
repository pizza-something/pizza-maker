from dataclasses import dataclass

from pizza_maker.entities.core.sauce import Sauce, SauceName
from pizza_maker.entities.quantities.milliliters import Milliliters


@dataclass(kw_only=True, frozen=True, slots=True)
class SauceDto:
    name: SauceName
    milliliters_number: int


def input_sauce_of(dto: SauceDto) -> Sauce:
    """
    :raises pizza_maker.entities.quantities.millimeters.NegaiveMillimetersError:
    """

    return Sauce(
        name=dto.name,
        milliliters=Milliliters(number=dto.milliliters_number),
    )
