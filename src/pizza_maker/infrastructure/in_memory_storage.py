from copy import deepcopy
from dataclasses import dataclass, field


class NoTranasctionError(Exception): ...


@dataclass(kw_only=True)
class TransactionalInMemoryStorage[ValueT]:
    storage: list[ValueT]
    _snapshots: list[list[ValueT]] = field(init=False)

    def begin(self) -> None:
        self._snapshots.append(deepcopy(self.storage))

    def commit(self) -> None:
        self._validate_has_snapshots()
        self._snapshots.pop()

    def rollback(self) -> None:
        self._validate_has_snapshots()
        snapshot = self._snapshots.pop()
        self.storage = snapshot

    def _validate_has_snapshots(self) -> None:
        if not self._snapshots:
            raise NoTranasctionError
