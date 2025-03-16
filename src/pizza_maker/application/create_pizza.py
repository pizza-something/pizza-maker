from dataclasses import dataclass

from pizza_maker.application.dtos.crust_dto import CrustDto, input_crust_of
from pizza_maker.application.dtos.ingredient_dto import (
    IngredientDto,
    input_ingredient_of,
)
from pizza_maker.application.dtos.sauce_dto import SauceDto, input_sauce_of
from pizza_maker.application.ports.clock import Clock
from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessTokenWhen,
)
from pizza_maker.application.ports.map import MapTo
from pizza_maker.application.ports.pizzas import Pizzas
from pizza_maker.application.ports.private_event_queue import (
    PizzaCreatedEvent,
    PrivateEventQueue,
)
from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.entities.core.pizza import Pizza, created_pizza_when
from pizza_maker.entities.framework.effect import New, just


@dataclass(kw_only=True, frozen=True, slots=True)
class CreatePizza[
    EncodedAccessTokenT, PizzasT: Pizzas, PrivateEventQueueT: PrivateEventQueue
]:
    clock: Clock
    decoded_access_token_when: DecodedAccessTokenWhen[EncodedAccessTokenT]
    pizzas: PizzasT
    private_event_queue: PrivateEventQueueT
    map_to: MapTo[tuple[PizzasT, ...], New[Pizza]]
    transaction_of: TransactionOf[tuple[PizzasT, PrivateEventQueueT]]

    async def __call__(
        self,
        encoded_access_token: EncodedAccessTokenT,
        sauce_dto: SauceDto,
        crust_dto: CrustDto,
        ingredient_dtos: tuple[IngredientDto, ...],
    ) -> None:
        """
        :raises pizza_maker.entities.quantities.millimeters.NegaiveMillimetersError:
        :raises pizza_maker.entities.quantities.milliliters.NegaiveMillilitersError:
        :raises pizza_maker.entities.quantities.grams.NegaiveGramsError:
        :raises pizza_maker.entities.access.access_token.AccessDeniedError:
        """  # noqa: E501

        current_time = await self.clock.get_current_time()

        ingredients = tuple(map(input_ingredient_of, ingredient_dtos))
        sauce = input_sauce_of(sauce_dto)
        crust = input_crust_of(crust_dto)

        access_token = await self.decoded_access_token_when(
            encoded_access_token=encoded_access_token
        )

        pizza = created_pizza_when(
            access_token=access_token,
            current_time=current_time,
            ingredients=ingredients,
            sauce=sauce,
            crust=crust,
        )

        event = PizzaCreatedEvent(pizza=just(pizza))

        async with self.transaction_of((self.pizzas, self.private_event_queue)):
            await self.map_to((self.pizzas, ), pizza)
            await self.private_event_queue.push(event)
