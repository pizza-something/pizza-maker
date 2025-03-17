from dataclasses import dataclass
from typing import Any

from pizza_maker.application.dtos.crust_data_dto import (
    CrustDataDto,
    input_crust_data_of,
)
from pizza_maker.application.dtos.ingredient_data_dto import (
    IngredientDataDto,
    input_ingredient_data_of,
)
from pizza_maker.application.dtos.sauce_dto import (
    SauceDataDto,
    input_sauce_data_of,
)
from pizza_maker.application.ports.clock import Clock
from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessTokenWhen,
)
from pizza_maker.application.ports.event_queue import (
    EventQueue,
    PizzaCreatedEvent,
)
from pizza_maker.application.ports.map import MapTo
from pizza_maker.application.ports.pizzas import Pizzas
from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.application.ports.users import Users
from pizza_maker.entities.common.effect import Effect, just
from pizza_maker.entities.core.pizza.crust import Crust
from pizza_maker.entities.core.pizza.ingredient import Ingredient
from pizza_maker.entities.core.pizza.pizza import Pizza, created_pizza_when
from pizza_maker.entities.core.pizza.sauce import Sauce


@dataclass(kw_only=True, frozen=True, slots=True)
class CreatePizza[
    EncodedAccessTokenT = Any,
    UsersT: Users = Users,
    PizzasT: Pizzas = Pizzas,
]:
    clock: Clock
    decoded_access_token_when: DecodedAccessTokenWhen[EncodedAccessTokenT]
    pizzas: PizzasT
    users: UsersT
    event_queue: EventQueue
    map_to: MapTo[
        tuple[PizzasT],
        Effect[Pizza, Pizza | Sauce | Ingredient | Crust]
    ]
    transaction_of: TransactionOf[tuple[PizzasT, UsersT]]

    async def __call__(
        self,
        encoded_access_token: EncodedAccessTokenT,
        sauce_data_dto: SauceDataDto,
        crust_data_dto: CrustDataDto,
        ingredient_data_dtos: tuple[IngredientDataDto, ...],
    ) -> None:
        """
        :raises pizza_maker.entities.units.millimeters.NegaiveMillimetersError:
        :raises pizza_maker.entities.units.milliliters.NegaiveMillilitersError:
        :raises pizza_maker.entities.units.grams.NegaiveGramsError:
        :raises pizza_maker.entities.access.access_token.AccessDeniedError:
        :raises pizza_maker.entities.core.user.NoUserForUserAuthenticationError:
        """

        current_time = await self.clock.get_current_time()

        ingredient_data_set = (
            tuple(map(input_ingredient_data_of, ingredient_data_dtos))
        )
        sauce_data = input_sauce_data_of(sauce_data_dto)
        crust_data = input_crust_data_of(crust_data_dto)
        access_token = await self.decoded_access_token_when(
            encoded_access_token=encoded_access_token
        )

        async with self.transaction_of((self.pizzas, self.users)):
            if access_token is None:
                user = None
            else:
                user = await self.users.user_with_id(access_token.user_id)

            pizza = created_pizza_when(
                access_token=access_token,
                current_time=current_time,
                ingredient_data_set=ingredient_data_set,
                sauce_data=sauce_data,
                crust_data=crust_data,
                user=user,
            )

            await self.map_to((self.pizzas, ), pizza)
            await self.event_queue.push(PizzaCreatedEvent(pizza=just(pizza)))
