from dataclasses import dataclass


class NegaiveMillilitersError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Milliliters:
    """
    :raises input.entities.quantities.milliliters.NegaiveMillilitersError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveMillilitersError
