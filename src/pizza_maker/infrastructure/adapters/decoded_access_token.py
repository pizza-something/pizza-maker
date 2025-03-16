from dataclasses import dataclass, field
from uuid import UUID

import jwt as pyjwt

from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessToken,
    DecodedAccessTokenWhen,
)
from pizza_maker.entities.access.access_token import AccessToken
from pizza_maker.entities.core.user import User
from pizza_maker.infrastructure.types import JWT


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

        user_id_hex: str | None = data.get("user_id")

        if user_id_hex is None:
            return None

        try:
            user_id = UUID(hex=user_id_hex)
        except ValueError:
            return None

        return AccessToken(user_id=user_id, expiration_time=)
