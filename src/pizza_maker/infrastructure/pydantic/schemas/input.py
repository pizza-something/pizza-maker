from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from pizza_maker.application.dtos.account_dto import AccountDto
from pizza_maker.application.dtos.crust_data_dto import CrustDataDto
from pizza_maker.application.dtos.ingredient_data_dto import IngredientDataDto
from pizza_maker.application.dtos.sauce_dto import SauceDataDto
from pizza_maker.entities.core.pizza.ingredient import IngredientName
from pizza_maker.entities.core.pizza.sauce import SauceName


class InputSchema[ValueT](BaseModel, ABC):
    @abstractmethod
    def as_dto(self) -> ValueT: ...


class InputAccountSchema(InputSchema[AccountDto]):
    id: UUID = Field(alias="id")

    def as_dto(self) -> AccountDto:
        return AccountDto(id=self.id)


class InputSauceSchema(InputSchema[SauceDataDto]):
    name: SauceName = Field(alias="name")
    milliliters_number: PositiveInt = Field(alias="milliliters")

    def as_dto(self) -> SauceDataDto:
        return SauceDataDto(
            name=self.name,
            milliliters_number=self.milliliters_number,
        )


class InputIngredientSchema(InputSchema[IngredientDataDto]):
    name: IngredientName = Field(alias="name")
    grams_number: PositiveInt = Field(alias="grams")

    def as_dto(self) -> IngredientDataDto:
        return IngredientDataDto(
            name=self.name,
            grams_number=self.grams_number,
        )


class InputCrustSchema(InputSchema[CrustDataDto]):
    thickness_millimeters_number: PositiveInt = Field(
        alias="thicknessMillimeters"
    )
    diameter_millimeters_number: PositiveInt = Field(
        alias="diameterMillimeters"
    )

    def as_dto(self) -> CrustDataDto:
        return CrustDataDto(
            thickness_millimeters_number=self.thickness_millimeters_number,
            diameter_millimeters_number=self.diameter_millimeters_number,
        )
