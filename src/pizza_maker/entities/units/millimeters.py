from dataclasses import dataclass


class NegaiveMillimetersError(Exception): ...


@dataclass(kw_only=True, frozen=True)
class Millimeters:
    """
    :raises input.entities.units.millimeters.NegaiveMillimetersError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveMillimetersError
