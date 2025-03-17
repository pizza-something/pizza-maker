from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

import jwt as pyjwt

from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessTokenWhen,
)
from pizza_maker.entities.access.access_token import AccessToken
from pizza_maker.entities.time.time import NotUTCTimeError, Time
from pizza_maker.infrastructure.types import JWT


@dataclass(kw_only=True, frozen=True, slots=True)
class DecodedAccessTokenFromAccessTokenWhen(
    DecodedAccessTokenWhen[AccessToken | None]
):
    async def __call__(
        self, *, encoded_access_token: AccessToken | None
    ) -> AccessToken | None:
        return encoded_access_token


@dataclass(kw_only=True, frozen=True, slots=True)
class DecodedAccessTokenFromHS256JWTWhen(DecodedAccessTokenWhen[JWT]):
    secret: str = field(repr=False)

    async def __call__(
        self, *, encoded_access_token: JWT
    ) -> AccessToken | None:
        jwt = encoded_access_token

        try:
            data = pyjwt.decode_complete(jwt, self.secret, algorithms="HS256")
        except pyjwt.DecodeError:
            return None

        header: dict[str, Any] = data["header"]
        payload: dict[str, Any] = data["payload"]

        user_id_hex: Any = payload.get("user_id")
        expiration_iso_time: Any = header.get("exp")

        try:
            user_id = UUID(hex=user_id_hex)
        except ValueError:
            return None

        try:
            expiration_datetime = datetime.fromisoformat(expiration_iso_time)
        except ValueError:
            return None
        except TypeError:
            return None

        try:
            expiration_time = Time(datetime=expiration_datetime)
        except NotUTCTimeError:
            return None

        return AccessToken(user_id=user_id, expiration_time=expiration_time)
