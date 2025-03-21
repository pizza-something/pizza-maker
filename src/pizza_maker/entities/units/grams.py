from dataclasses import dataclass


class NegaiveGramsError(Exception): ...


@dataclass(kw_only=True, frozen=True)
class Grams:
    """
    :raises input.entities.units.grams.NegaiveGramsError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveGramsError
