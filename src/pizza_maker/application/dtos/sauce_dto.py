from dataclasses import dataclass

from pizza_maker.entities.core.pizza.sauce import SauceData, SauceName
from pizza_maker.entities.units.milliliters import Milliliters


@dataclass(kw_only=True, frozen=True, slots=True)
class SauceDataDto:
    name: SauceName
    milliliters_number: int


def input_sauce_data_of(dto: SauceDataDto) -> SauceData:
    """
    :raises pizza_maker.entities.units.millimeters.NegaiveMillimetersError:
    """

    return SauceData(
        name=dto.name,
        milliliters=Milliliters(number=dto.milliliters_number),
    )
