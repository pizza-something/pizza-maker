from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class AccessToken:
    user_id: UUID
    expiration_time: Time


@dataclass(kw_only=True, frozen=True)
class ValidAccessToken:
    user_id: UUID


def is_expired(
    access_token: AccessToken, *, current_time: Time
) -> bool:
    return access_token.expiration_time <= current_time


class InvalidAccessTokenForAuthenticationError(Exception): ...


def valid(
    access_token: AccessToken | None,
    *,
    current_time: Time,
) -> ValidAccessToken:
    """
    :raises pizza_maker.entities.access.access_token.InvalidAccessTokenForAuthenticationError:
    """  # noqa: E501

    if access_token is None:
        raise InvalidAccessTokenForAuthenticationError

    if is_expired(access_token, current_time=current_time):
        raise InvalidAccessTokenForAuthenticationError

    return ValidAccessToken(user_id=access_token.user_id)
