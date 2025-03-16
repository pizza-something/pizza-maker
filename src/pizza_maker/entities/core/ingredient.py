from dataclasses import dataclass
from enum import Enum, auto

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
class Ingredient:
    name: IngredientName
    grams: Grams
