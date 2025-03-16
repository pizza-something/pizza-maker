from dataclasses import dataclass

from pizza_maker.entities.core.crust import Crust
from pizza_maker.entities.quantities.millimeters import Millimeters


@dataclass(kw_only=True, frozen=True, slots=True)
class CrustDto:
    thickness_millimeters_number: int
    diameter_millimeters_number: int


def input_crust_of(dto: CrustDto) -> Crust:
    """
    :raises pizza_maker.entities.quantities.millimeters.NegaiveMillimetersError:
    """

    return Crust(
        thickness=Millimeters(number=dto.thickness_millimeters_number),
        diameter=Millimeters(number=dto.diameter_millimeters_number),
    )
