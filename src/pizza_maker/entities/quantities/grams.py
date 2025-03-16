from dataclasses import dataclass


class NegaiveGramsError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Grams:
    """
    :raises input.entities.quantities.grams.NegaiveGramsError:
    """

    number: int

    def __post_init__(self) -> None:
        if self.number < 0:
            raise NegaiveGramsError
