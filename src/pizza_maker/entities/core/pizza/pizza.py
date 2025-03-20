from dataclasses import dataclass
from uuid import UUID, uuid4

from pizza_maker.entities.access.access_token import AccessToken
from pizza_maker.entities.common.effect import Effect, just, many, new
from pizza_maker.entities.common.identified import Identified
from pizza_maker.entities.core.pizza.crust import (
    Crust,
    CrustData,
    new_crust_when,
)
from pizza_maker.entities.core.pizza.ingredient import (
    Ingredient,
    IngredientData,
    new_ingredient_when,
)
from pizza_maker.entities.core.pizza.sauce import (
    Sauce,
    SauceData,
    new_sauce_when,
)
from pizza_maker.entities.core.user import (
    User,
    authenticated_user_when,
)
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class Pizza(Identified[UUID]):
    id: UUID
    user_id: UUID
    sauce: Sauce
    crust: Crust
    ingredients: tuple[Ingredient, ...]


type PizzaAggregate = Pizza | Sauce | Crust | Ingredient


def created_pizza_when(
    *,
    access_token: AccessToken | None,
    user: User | None,
    current_time: Time,
    sauce_data: SauceData,
    crust_data: CrustData,
    ingredient_data_set: tuple[IngredientData, ...],
) -> Effect[Pizza, Pizza | Sauce | Ingredient | Crust]:
    """
    :raises pizza_maker.entities.access.access_token.InvalidAccessTokenForAuthenticationError:
    :raises pizza_maker.entities.core.user.NoUserForUserAuthenticationError:
    """  # noqa: E501

    user = authenticated_user_when(
        user=user, access_token=access_token, current_time=current_time
    )
    pizza_id = uuid4()
    sauce = new_sauce_when(sauce=None, sauce_data=sauce_data, pizza_id=pizza_id)
    crust = new_crust_when(crust=None, crust_data=crust_data, pizza_id=pizza_id)
    ingredients = many(
        new_ingredient_when(ingredient_data=ingredient_data, pizza_id=pizza_id)
        for ingredient_data in ingredient_data_set
    )
    pizza = new(Pizza(
        id=pizza_id,
        user_id=user.id,
        sauce=just(sauce),
        crust=just(crust),
        ingredients=just(ingredients),
    ))

    return sauce & crust & ingredients & pizza
