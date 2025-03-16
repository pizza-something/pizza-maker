from dataclasses import dataclass

from pizza_maker.entities.core.ingredient import Ingredient, IngredientName
from pizza_maker.entities.quantities.grams import Grams


@dataclass(kw_only=True, frozen=True, slots=True)
class IngredientDto:
    name: IngredientName
    grams_number: int


def input_ingredient_of(dto: IngredientDto) -> Ingredient:
    """
    :raises pizza_maker.entities.quantities.grams.NegaiveGramsError:
    """

    return Ingredient(
        name=dto.name,
        grams=Grams(number=dto.grams_number),
    )
