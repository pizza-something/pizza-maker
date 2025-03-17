from dataclasses import dataclass

from pizza_maker.entities.core.pizza.ingredient import IngredientData, IngredientName
from pizza_maker.entities.quantities.grams import Grams


@dataclass(kw_only=True, frozen=True, slots=True)
class IngredientDataDto:
    name: IngredientName
    grams_number: int


def input_ingredient_data_of(dto: IngredientDataDto) -> IngredientData:
    """
    :raises pizza_maker.entities.quantities.grams.NegaiveGramsError:
    """

    return IngredientData(
        name=dto.name,
        grams=Grams(number=dto.grams_number),
    )
