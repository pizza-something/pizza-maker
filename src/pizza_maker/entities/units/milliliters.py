from dataclasses import dataclass


class NegaiveMillilitersError(Exception): ...


@dataclass(kw_only=True, frozen=True)
class Milliliters:
    """
    :raises input.entities.units.milliliters.NegaiveMillilitersError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveMillilitersError
