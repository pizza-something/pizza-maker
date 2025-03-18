from collections.abc import Sequence

from pizza_maker.application.ports.map import MapTo
from pizza_maker.entities.common.effect import LifeCycle
from pizza_maker.entities.core.pizza.crust import Crust
from pizza_maker.entities.core.pizza.ingredient import Ingredient
from pizza_maker.entities.core.pizza.pizza import Pizza
from pizza_maker.entities.core.pizza.sauce import Sauce
from pizza_maker.entities.core.user import User
from pizza_maker.infrastructure.sqlalchemy.driver import (
    PostgresDriver,
    session_of,
)


type InPostgresEntityLifeCycle = (
    LifeCycle[User]
    | LifeCycle[Pizza]
    | LifeCycle[Sauce]
    | LifeCycle[Crust]
    | LifeCycle[Ingredient]
)


class MapToPostgres(
    MapTo[Sequence[PostgresDriver], InPostgresEntityLifeCycle]
):
    async def __call__(
        self,
        storages: Sequence[PostgresDriver],
        effect: InPostgresEntityLifeCycle,
    ) -> None:
        session = session_of(storages)

        session.add_all(effect.new_values)

        for dirty_value in effect.dirty_values:
            await session.merge(dirty_value, load=False)

        for deleted_value in effect.deleted_values:
            await session.delete(deleted_value)

        await session.flush()
