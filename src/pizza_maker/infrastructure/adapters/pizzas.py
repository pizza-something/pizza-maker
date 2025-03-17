from dataclasses import dataclass

from pizza_maker.application.ports.pizzas import Pizzas
from pizza_maker.infrastructure.sqlalchemy.driver import PostgresDriver


class NoPizzas(Pizzas): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresPizzas(Pizzas, PostgresDriver): ...
