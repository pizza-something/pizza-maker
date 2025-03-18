from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.access.access_token import (
    AccessToken,
    InvalidAccessTokenForAuthenticationError,
    valid,
)
from pizza_maker.entities.access.account import Account
from pizza_maker.entities.common.effect import Existing, New, existing, new
from pizza_maker.entities.common.identified import Identified
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class User(Identified[UUID]):
    id: UUID


def new_user_when(
    *, user: User | None, account: Account
) -> New[User] | Existing[User]:
    if user is not None:
        return existing(user)

    return new(User(id=account.id))


class NoUserForUserAuthenticationError(Exception): ...


def authenticated_user_when(
    *,
    user: User | None,
    access_token: AccessToken | None,
    current_time: Time,
) -> User:
    """
    :raises pizza_maker.entities.access.access_token.InvalidAccessTokenForAuthenticationError:
    :raises pizza_maker.entities.core.user.NoUserForUserAuthenticationError:
    """  # noqa: E501

    valid_access_token = valid(access_token, current_time=current_time)

    if user is None:
        raise NoUserForUserAuthenticationError

    if user.id != valid_access_token.user_id:
        raise InvalidAccessTokenForAuthenticationError

    return user
