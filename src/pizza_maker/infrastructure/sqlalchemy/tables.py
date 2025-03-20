from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Uuid,
)
from sqlalchemy.dialects import postgresql

from pizza_maker.entities.core.pizza.ingredient import IngredientName
from pizza_maker.entities.core.pizza.sauce import SauceName


metadata = MetaData()

sauce_name = postgresql.ENUM(SauceName, name="sauce_name")
ingredient_name = postgresql.ENUM(IngredientName, name="ingredient_name")

user_table = Table(
    "users",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
)

pizza_table = Table(
    "pizzas",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

sauce_table = Table(
    "sauces",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("pizza_id", ForeignKey("pizzas.id"), nullable=False),
    Column("name", sauce_name, nullable=False),
    Column("milliliters", Integer(), nullable=False),
)

crust_table = Table(
    "crusts",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("pizza_id", ForeignKey("pizzas.id"), nullable=False),
    Column("thickness", Integer(), nullable=False),
    Column("diameter", Integer(), nullable=False),
)

ingredient_table = Table(
    "ingredients",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("pizza_id", ForeignKey("pizzas.id"), nullable=False),
    Column("name", ingredient_name, nullable=False),
    Column("grams", Integer(), nullable=False),
)
