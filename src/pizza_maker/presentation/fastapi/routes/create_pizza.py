from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from pizza_maker.application.create_pizza import CreatePizza
from pizza_maker.entities.access.access_token import (
    InvalidAccessTokenForAuthenticationError,
)
from pizza_maker.entities.core.user import NoUserForUserAuthenticationError
from pizza_maker.infrastructure.pydantic.schemas.common import NoDataSchema
from pizza_maker.infrastructure.pydantic.schemas.input import (
    InputCrustSchema,
    InputIngredientSchema,
    InputSauceSchema,
)
from pizza_maker.presentation.fastapi.cookies import AccessTokenCookie
from pizza_maker.presentation.fastapi.schemas.errors import (
    ErrorListSchema,
    InvalidAccessTokenSchema,
    NoUserSchema,
)
from pizza_maker.presentation.fastapi.tags import Tag


create_pizza_router = APIRouter()


class RegisterUserSchema(BaseModel):
    user_name: str = Field(alias="userName")


class CreatePizzaSchema(BaseModel):
    sauce: InputSauceSchema
    crust: InputCrustSchema
    ingredients: tuple[InputIngredientSchema, ...]


@create_pizza_router.post(
    "/pizza",
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorListSchema[NoUserSchema]
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorListSchema[InvalidAccessTokenSchema]
        },
    },
    summary="Create pizza",
    description="Create a pizza for a current user.",
    tags=[Tag.user, Tag.pizza],
)
@inject
async def create_pizza_route(
    create_pizza: FromDishka[CreatePizza[str]],
    request_body: CreatePizzaSchema,
    encoded_access_token: AccessTokenCookie.Str,
) -> Response:
    response_body_model: BaseModel

    try:
        await create_pizza(
            encoded_access_token,
            request_body.sauce.as_dto(),
            request_body.crust.as_dto(),
            tuple(it.as_dto() for it in request_body.ingredients),
        )
    except InvalidAccessTokenForAuthenticationError:
        response_body_model = InvalidAccessTokenSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse(response_body, status_code=status_code)
    except NoUserForUserAuthenticationError:
        response_body_model = NoUserSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_404_NOT_FOUND
        return JSONResponse(response_body, status_code=status_code)

    return JSONResponse({}, status_code=status.HTTP_201_CREATED)
