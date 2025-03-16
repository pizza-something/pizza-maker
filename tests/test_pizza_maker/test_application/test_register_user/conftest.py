from uuid import UUID

from pytest import fixture

from pizza_maker.application.register_user import RegisterUser
from pizza_maker.entities.core.user import User
from pizza_maker.infrastructure.adapters.user_data_signing import (
    UserDataSigningAsIdentification,
)
from pizza_maker.infrastructure.adapters.users import InMemoryUsers


@fixture
def register_user() -> RegisterUser[User | None]:
    return RegisterUser(
        user_data_signing=UserDataSigningAsIdentification(),
        users=InMemoryUsers(_user_set=set()),
    )


@fixture
def registered_user() -> User:
    return User(id=UUID(int=0), name="X")
