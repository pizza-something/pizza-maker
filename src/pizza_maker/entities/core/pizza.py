from dataclasses import dataclass
from typing import Never
from uuid import UUID, uuid4

from pizza_maker.entities.access.access_token import AccessToken
from pizza_maker.entities.core.crust import Crust
from pizza_maker.entities.core.ingredient import Ingredient
from pizza_maker.entities.core.sauce import Sauce
from pizza_maker.entities.core.user import User, user_when
from pizza_maker.entities.framework.effect import (
    Effect,
    Existing,
    New,
    just,
    new,
)
from pizza_maker.entities.framework.identified import Identified
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class Pizza(Identified[UUID]):
    id: UUID
    user_id: UUID
    sauce: Sauce
    crust: Crust
    ingredients: tuple[Ingredient, ...]


def created_pizza_when(
    *,
    access_token: AccessToken | None,
    user: User | None,
    current_time: Time,
    sauce: Sauce,
    crust: Crust,
    ingredients: tuple[Ingredient, ...],
) -> New[Pizza] | Effect[Pizza, Pizza | User]:
    """
    :raises pizza_maker.entities.access.access_token.AccessDeniedError:
    """

    user: New[User] | Existing[User] = user_when(
        user=user, access_token=access_token, current_time=current_time
    )

    return user & new(Pizza(
        id=uuid4(),
        user_id=just(user).id,
        sauce=sauce,
        crust=crust,
        ingredients=ingredients,
    ))
