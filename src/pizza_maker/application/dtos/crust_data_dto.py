from dataclasses import dataclass

from pizza_maker.entities.core.pizza.crust import CrustData
from pizza_maker.entities.units.millimeters import Millimeters


@dataclass(kw_only=True, frozen=True, slots=True)
class CrustDataDto:
    thickness_millimeters_number: int
    diameter_millimeters_number: int


def input_crust_data_of(dto: CrustDataDto) -> CrustData:
    """
    :raises pizza_maker.entities.units.millimeters.NegaiveMillimetersError:
    """

    return CrustData(
        thickness=Millimeters(number=dto.thickness_millimeters_number),
        diameter=Millimeters(number=dto.diameter_millimeters_number),
    )
