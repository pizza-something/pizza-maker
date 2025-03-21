from dataclasses import dataclass
from enum import Enum, auto
from uuid import UUID, uuid4

from effect import Identified, Mutated, New, mutated, new

from pizza_maker.entities.units.grams import Grams


class IngredientName(Enum):
    # chesee
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

    # meat
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

    # seafood
    anchovies = auto()
    shrimp = auto()
    smoked_salmon = auto()
    tuna = auto()
    seaweed = auto()

    # herb
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


cheese_names = (
    IngredientName.mozzarella,
    IngredientName.parmesan,
    IngredientName.ricotta,
    IngredientName.gorgonzola,
    IngredientName.cheddar,
    IngredientName.feta,
    IngredientName.provolone,
    IngredientName.burrata,
    IngredientName.brie,
    IngredientName.goat_cheese,
    IngredientName.vegan_cheese,
)


meat_names = (
    IngredientName.pepperoni,
    IngredientName.ham,
    IngredientName.bacon,
    IngredientName.sausage,
    IngredientName.chorizo,
    IngredientName.salami,
    IngredientName.grilled_chicken,
    IngredientName.prosciutto,
    IngredientName.ground_beef,
    IngredientName.calabrese_sausage,
)


seafood_names = (
    IngredientName.anchovies,
    IngredientName.shrimp,
    IngredientName.smoked_salmon,
    IngredientName.tuna,
    IngredientName.seaweed,
)


herb_names = (
    IngredientName.mushrooms,
    IngredientName.bell_peppers,
    IngredientName.red_onion,
    IngredientName.black_olives,
    IngredientName.jalape_os,
    IngredientName.spinach,
    IngredientName.artichokes,
    IngredientName.arugula,
    IngredientName.sun_dried_tomatoes,
    IngredientName.cherry_tomatoes,
    IngredientName.zucchini,
    IngredientName.eggplant,
    IngredientName.broccoli,
    IngredientName.capers,
    IngredientName.basil,
    IngredientName.garlic,
    IngredientName.pineapple,
    IngredientName.corn,
    IngredientName.potato_slices,
    IngredientName.asparagus,
)


@dataclass(kw_only=True, frozen=True)
class Ingredient(Identified[UUID]):
    id: UUID
    pizza_id: UUID
    name: IngredientName
    grams: Grams


@dataclass(kw_only=True, frozen=True)
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
) -> Mutated[Ingredient]:
    return mutated(Ingredient(
        id=ingredient.id,
        name=ingredient_data.name,
        grams=ingredient_data.grams,
        pizza_id=pizza_id,
    ))
