from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)
from pizza_maker.infrastructure.sqlalchemy.driver import (
    PostgresDriver,
    session_of,
)


class InPostgresTransactionOf(TransactionOf[Sequence[PostgresDriver]]):
    @asynccontextmanager
    async def __call__(
        self, storages: Sequence[PostgresDriver]
    ) -> AsyncIterator[None]:
        async with session_of(storages).begin():
            yield


class InMemoryTransactionOf(
    TransactionOf[Sequence[TransactionalInMemoryStorage[Any]]]
):
    @asynccontextmanager
    async def __call__(
        self, storages: Sequence[TransactionalInMemoryStorage[Any]]
    ) -> AsyncIterator[None]:
        for storage in storages:
            storage.begin()

        try:
            yield
        except Exception as error:
            for storage in storages:
                storage.rollback()
            raise error from error
        else:
            for storage in storages:
                storage.commit()
