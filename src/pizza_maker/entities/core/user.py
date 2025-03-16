from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.access.access_token import (
    AccessDeniedError,
    AccessToken,
    valid,
)
from pizza_maker.entities.framework.effect import Existing, New, existing, new
from pizza_maker.entities.framework.identified import Identified
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class User(Identified[UUID]):
    id: UUID


class InvalidAccessTokenError(Exception): ...


def user_when(
    *,
    user: User | None,
    access_token: AccessToken | None,
    current_time: Time,
) -> New[User] | Existing[User]:
    """
    :raises pizza_maker.entities.access.access_token.AccessDeniedError:
    """

    valid_access_token = valid(access_token, current_time=current_time)

    if user is None:
        return new(User(id=valid_access_token.user_id))

    if user.id != valid_access_token.user_id:
        raise AccessDeniedError

    return existing(user)
