from dataclasses import dataclass
from datetime import UTC, datetime


class NotUTCTimeError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Time:
    """
    :raises pizza_maker.entities.time.time.NotUTCTimeError:
    """

    datetime: datetime

    def __post_init__(self) -> None:
        if self.datetime.tzinfo != UTC:
            raise NotUTCTimeError

    def __gt__(self, time: "Time") -> bool:
        return self.datetime > time.datetime

    def __ge__(self, time: "Time") -> bool:
        return self.datetime >= time.datetime
