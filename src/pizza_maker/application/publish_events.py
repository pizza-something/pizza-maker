from dataclasses import dataclass

from pizza_maker.application.ports.private_event_queue import PrivateEventQueue
from pizza_maker.application.ports.public_event_queue import PublicEventQueue
from pizza_maker.application.ports.transaction import TransactionOf


@dataclass(kw_only=True, frozen=True, slots=True)
class PublishEvents[
    PrivateEventQueueT: PrivateEventQueue[BatchT],
    PublicEventQueueT: PublicEventQueue[BatchT],
]:
    private_event_queue: PrivateEventQueueT
    public_event_queue: PublicEventQueueT
    transaction_of: TransactionOf[tuple[PrivateEventQueueT, ...]]

    async def __call__(self) -> None:
        while True:
            transaction = self.transaction_of((self.private_event_queue, ))
            commitable_batch = self.private_event_queue.pull_commitable_batch()

            async with transaction, commitable_batch as batch:
                if len(batch) == 0:
                    return

                await self.public_event_queue.push_batch(batch)
