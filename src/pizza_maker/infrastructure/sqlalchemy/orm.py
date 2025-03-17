from sqlalchemy.orm import (
    composite,
    registry,
    relationship,
)

from pizza_maker.entities.core.pizza.crust import Crust
from pizza_maker.entities.core.pizza.ingredient import Ingredient
from pizza_maker.entities.core.pizza.pizza import Pizza
from pizza_maker.entities.core.pizza.sauce import Sauce
from pizza_maker.entities.core.user import User
from pizza_maker.entities.units.grams import Grams
from pizza_maker.entities.units.milliliters import Milliliters
from pizza_maker.infrastructure.sqlalchemy.tables import (
    crust_table,
    ingredient_table,
    metadata,
    pizza_table,
    sauce_table,
    user_table,
)


mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(User, user_table)

mapper_registry.map_imperatively(
    Pizza,
    pizza_table,
    properties=dict(
        id=pizza_table.c.id,
        user_id=pizza_table.c.user_id,
        sauce=relationship(Sauce),
        crust=relationship(Crust),
        ingredients=relationship(Ingredient, use_list=True)
    )
)

mapper_registry.map_imperatively(
    Sauce,
    sauce_table,
    properties=dict(
        id=sauce_table.c.id,
        pizza_id=sauce_table.c.pizza_id,
        name=sauce_table.c.name,
        milliliters=composite(Milliliters, sauce_table.c.milliliters),
    )
)

mapper_registry.map_imperatively(
    Crust,
    crust_table,
    properties=dict(
        id=crust_table.c.id,
        pizza_id=crust_table.c.pizza_id,
        thickness=composite(Milliliters, crust_table.c.thickness),
        diameter=composite(Milliliters, crust_table.c.diameter),
    )
)

mapper_registry.map_imperatively(
    Ingredient,
    ingredient_table,
    properties=dict(
        id=ingredient_table.c.id,
        pizza_id=ingredient_table.c.pizza_id,
        name=ingredient_table.c.name,
        grams=composite(Grams, ingredient_table.c.grams),
    )
)
