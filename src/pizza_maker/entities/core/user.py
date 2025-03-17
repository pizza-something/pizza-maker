from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.access.access_token import (
    AccessDeniedError,
    AccessToken,
    valid,
)
from pizza_maker.entities.access.account import Account
from pizza_maker.entities.framework.effect import New, new
from pizza_maker.entities.framework.identified import Identified
from pizza_maker.entities.time.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class User(Identified[UUID]):
    id: UUID


class InvalidAccessTokenError(Exception): ...


class RegisteredUserForUserRegistrationError(Exception): ...


def registered_user_when(*, user: User | None, account: Account) -> New[User]:
    """
    :raises pizza_maker.entities.core.user.RegisteredUserForUserRegistrationError:
    """  # noqa: E501

    if user is not None:
        raise RegisteredUserForUserRegistrationError

    return new(User(id=account.id))


class NoUserForUserAuthenticationError(Exception): ...


def authenticated_user_when(
    *,
    user: User | None,
    access_token: AccessToken | None,
    current_time: Time,
) -> User:
    """
    :raises pizza_maker.entities.access.access_token.AccessDeniedError:
    :raises pizza_maker.entities.core.user.NoUserForUserAuthenticationError:
    """

    valid_access_token = valid(access_token, current_time=current_time)

    if user is None:
        raise NoUserForUserAuthenticationError

    if user.id != valid_access_token.user_id:
        raise AccessDeniedError

    return user
