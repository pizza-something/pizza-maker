from dataclasses import dataclass

from pizza_maker.application.ports.private_event_queue import PrivateEventQueue
from pizza_maker.application.ports.public_event_queue import PublicEventQueue


@dataclass(kw_only=True, frozen=True, slots=True)
class PublishEvents:
    private_event_queue: PrivateEventQueue
    public_event_queue: PublicEventQueue

    async def __call__(self) -> None:
        while True:
            commitable_batch = self.private_event_queue.pull_commitable_batch()

            async with commitable_batch as batch:
                if len(batch) == 0:
                    return

                await self.public_event_queue.push_batch(batch)
