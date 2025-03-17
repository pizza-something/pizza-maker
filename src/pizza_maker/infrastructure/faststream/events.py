from uuid import UUID

from pydantic import BaseModel, PositiveInt

from pizza_maker.application.ports.event_queue import Event, PizzaCreatedEvent
from pizza_maker.entities.core.pizza.sauce import SauceName


class UnhandlendEventError(Exception): ...


def kafka_event_and_topic_of(event: Event) -> tuple[BaseModel, str]:
    match event:
        case PizzaCreatedEvent() as event:
            return PizzaCreatedKafkaEvent.and_topic_of(event)
        case _:
            raise UnhandlendEventError


class PizzaCreatedKafkaEvent(BaseModel):
    pizza_id: UUID
    pizza_user_id: UUID
    pizza_sauce_name: SauceName
    pizza_sauce_milliliters: PositiveInt
    pizza_crust_thickness_millimeters: PositiveInt
    pizza_crust_diameter_millimeters: PositiveInt

    @classmethod
    def and_topic_of(
        cls, event: PizzaCreatedEvent
    ) -> tuple["PizzaCreatedKafkaEvent", str]:
        kafka_event = PizzaCreatedKafkaEvent(
            pizza_id=event.pizza.id,
            pizza_user_id=event.pizza.user_id,
            pizza_sauce_name=event.pizza.sauce.name,
            pizza_sauce_milliliters=event.pizza.sauce.milliliters.number,
            pizza_crust_thickness_millimeters=event.pizza.crust.thickness.number,
            pizza_crust_diameter_millimeters=event.pizza.crust.diameter.number,
        )

        return kafka_event, "pizza_created"
