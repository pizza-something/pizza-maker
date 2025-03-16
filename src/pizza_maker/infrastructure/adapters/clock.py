from dataclasses import dataclass
from datetime import UTC, datetime

from pizza_maker.application.ports.clock import Clock
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class StoppedClock(Clock):
    current_time: Time

    async def get_current_time(self) -> Time:
        return self.current_time


@dataclass(kw_only=True, frozen=True, slots=True)
class LocalHostClock(Clock):
    async def get_current_time(self) -> Time:
        return Time(datetime=datetime.now(UTC))
