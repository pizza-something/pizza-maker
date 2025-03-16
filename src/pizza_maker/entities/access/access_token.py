from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class AccessToken:
    user_id: UUID
    expiration_time: Time


@dataclass(kw_only=True, frozen=True, slots=True)
class ValidAccessToken:
    user_id: UUID


def is_expired(
    access_token: AccessToken, *, current_time: Time
) -> bool:
    return access_token.expiration_time <= current_time


class AccessDeniedError(Exception): ...


def valid(
    access_token: AccessToken | None,
    *,
    current_time: Time,
) -> ValidAccessToken:
    """
    :raises pizza_maker.entities.access.access_token.AccessDeniedError:
    """

    if access_token is None:
        raise AccessDeniedError

    if is_expired(access_token, current_time=current_time):
        raise AccessDeniedError

    return ValidAccessToken(user_id=access_token.user_id)
