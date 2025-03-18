from typing import Literal, Self

from pydantic import BaseModel, Field


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))


class InvalidAccessTokenSchema(ErrorSchema):
    type: Literal["invalidAccessToken"] = "invalidAccessToken"


class NoUserSchema(ErrorSchema):
    type: Literal["NoUser"] = "NoUser"
