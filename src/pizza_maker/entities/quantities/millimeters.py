from dataclasses import dataclass


class NegaiveMillimetersError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Millimeters:
    """
    :raises input.entities.quantities.millimeters.NegaiveMillimetersError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveMillimetersError
