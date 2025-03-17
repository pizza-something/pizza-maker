from abc import ABC, abstractmethod


class PublicEventQueue[EventBatchT](ABC):
    @abstractmethod
    async def push_batch(self, event_batch: EventBatchT) -> None: ...
