from dishka.integrations.faststream import FromDishka

from pizza_maker.application.on_account_created import OnAccountCreated
from pizza_maker.infrastructure.pydantic.schemas.input import InputAccountSchema
from pizza_maker.presentation.faststream.routes.default_route import (
    default_route_of,
)


@default_route_of("account.created.ok")
async def on_account_created_route(
    event: InputAccountSchema,
    on_account_created: FromDishka[OnAccountCreated]
) -> None:
    await on_account_created(event.as_dto())
