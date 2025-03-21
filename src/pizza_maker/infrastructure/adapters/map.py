from collections.abc import Sequence

from pizza_maker.application.ports.map import AggregateLifeCycle, MapTo
from pizza_maker.infrastructure.sqlalchemy.driver import (
    PostgresDriver,
    single_session_of,
)


class MapToPostgres(MapTo[Sequence[PostgresDriver]]):
    async def __call__(
        self,
        postgres_drivers: Sequence[PostgresDriver],
        effect: AggregateLifeCycle,
    ) -> None:
        session = single_session_of(postgres_drivers)

        session.add_all(effect.new_values)

        for mutated_value in effect.  mutated_values:
            await session.merge(mutated_value, load=False)

        for deleted_value in effect.deleted_values:
            await session.delete(deleted_value)

        await session.flush()
