from abc import ABC, abstractmethod
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from pizza_maker.entities.core.pizza.crust import Crust
from pizza_maker.entities.core.pizza.ingredient import Ingredient
from pizza_maker.entities.core.pizza.pizza import Pizza
from pizza_maker.entities.core.pizza.sauce import Sauce


class OutputSchema[ValueT](BaseModel, ABC):
    @classmethod
    @abstractmethod
    def of(cls, value: ValueT, /) -> Self: ...


class OutputCrustSchema(OutputSchema[Crust]):
    id: UUID = Field(alias="id")
    pizza_id: UUID = Field(alias="pizzaId")
    thickness: PositiveInt = Field(alias="thickness")
    diameter_millimeters_number: PositiveInt = Field(
        alias="diameterMillimeters"
    )

    @classmethod
    def of(cls, crust: Crust) -> "OutputCrustSchema":
        return cls(
            id=crust.id,
            pizzaId=crust.pizza_id,
            thickness=crust.thickness.number,
            diameterMillimeters=crust.diameter.number,
        )


class OutputIngredientSchema(OutputSchema[Ingredient]):
    id: UUID = Field(alias="id")
    pizza_id: UUID = Field(alias="pizzaId")
    name: str = Field(alias="name")
    grams: PositiveInt = Field(alias="grams")

    @classmethod
    def of(cls, ingredient: Ingredient) -> "OutputIngredientSchema":
        return cls(
            id=ingredient.id,
            pizzaId=ingredient.pizza_id,
            name=ingredient.name.name,
            grams=ingredient.grams.number,
        )


class OutputSauceSchema(OutputSchema[Sauce]):
    id: UUID = Field(alias="id")
    pizza_id: UUID = Field(alias="pizzaId")
    name: str = Field(alias="name")
    milliliters: PositiveInt = Field(alias="milliliters")

    @classmethod
    def of(cls, sauce: Sauce) -> "OutputSauceSchema":
        return cls(
            id=sauce.id,
            pizzaId=sauce.pizza_id,
            name=sauce.name.name,
            milliliters=sauce.milliliters.number,
        )


class OutputPizzaSchema(OutputSchema[Pizza]):
    id: UUID = Field(alias="id")
    user_id: UUID = Field(alias="userId")
    sauce: OutputSauceSchema = Field(alias="sauce")
    crust: OutputCrustSchema = Field(alias="crust")
    ingredients: tuple[OutputIngredientSchema, ...] = Field(alias="ingredients")

    @classmethod
    def of(cls, pizza: Pizza) -> "OutputPizzaSchema":
        return cls(
            id=pizza.id,
            userId=pizza.user_id,
            sauce=OutputSauceSchema.of(pizza.sauce),
            crust=OutputCrustSchema.of(pizza.crust),
            ingredients=tuple(
                OutputIngredientSchema.of(ingredient)
                for ingredient in pizza.ingredients
            ),
        )
