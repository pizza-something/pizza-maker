from dataclasses import dataclass
from enum import Enum, auto
from uuid import UUID, uuid4

from pizza_maker.entities.framework.effect import Dirty, New, dirty, new
from pizza_maker.entities.framework.identified import Identified
from pizza_maker.entities.quantities.grams import Grams


class CheeseName(Enum):
    mozzarella = auto()
    parmesan = auto()
    ricotta = auto()
    gorgonzola = auto()
    cheddar = auto()
    feta = auto()
    provolone = auto()
    burrata = auto()
    brie = auto()
    goat_cheese = auto()
    vegan_cheese = auto()


class MeatName(Enum):
    pepperoni = auto()
    ham = auto()
    bacon = auto()
    sausage = auto()
    chorizo = auto()
    salami = auto()
    grilled_chicken = auto()
    prosciutto = auto()
    ground_beef = auto()
    calabrese_sausage = auto()


class SeafoodName(Enum):
    anchovies = auto()
    shrimp = auto()
    smoked_salmon = auto()
    tuna = auto()
    seaweed = auto()


class HerbName(Enum):
    mushrooms = auto()
    bell_peppers = auto()
    red_onion = auto()
    black_olives = auto()
    jalape_os = auto()
    spinach = auto()
    artichokes = auto()
    arugula = auto()
    sun_dried_tomatoes = auto()
    cherry_tomatoes = auto()
    zucchini = auto()
    eggplant = auto()
    broccoli = auto()
    capers = auto()
    basil = auto()
    garlic = auto()
    pineapple = auto()
    corn = auto()
    potato_slices = auto()
    asparagus = auto()


type IngredientName = CheeseName | MeatName | SeafoodName | HerbName


@dataclass(kw_only=True, frozen=True, slots=True)
class Ingredient(Identified[UUID]):
    id: UUID
    pizza_id: UUID
    name: IngredientName
    grams: Grams


@dataclass(kw_only=True, frozen=True, slots=True)
class IngredientData:
    name: IngredientName
    grams: Grams


def new_ingredient_when(
    *,
    ingredient_data: IngredientData,
    pizza_id: UUID,
) -> New[Ingredient]:
    return new(Ingredient(
        id=uuid4(),
        name=ingredient_data.name,
        grams=ingredient_data.grams,
        pizza_id=pizza_id,
    ))


def changed_ingredient_when(
    *,
    ingredient: Ingredient,
    ingredient_data: IngredientData,
    pizza_id: UUID,
) -> Dirty[Ingredient]:
    return dirty(Ingredient(
        id=ingredient.id,
        name=ingredient_data.name,
        grams=ingredient_data.grams,
        pizza_id=pizza_id,
    ))
