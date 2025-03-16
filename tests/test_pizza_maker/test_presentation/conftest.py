from dishka import AsyncContainer, Provider, Scope, make_async_container
from pytest import fixture

from pizza_maker.application.ports.user_data_signing import (
    UserDataSigning,
)
from pizza_maker.application.ports.users import Users
from pizza_maker.application.register_user import RegisterUser
from pizza_maker.application.view_user import ViewUser
from pizza_maker.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pizza_maker.infrastructure.adapters.users import InMemoryUsers


@fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(
        lambda: UserDataSigningToHS256JWT(secret="super secret secret"),
        provides=UserDataSigning[str],
    )
    provider.provide(lambda: InMemoryUsers(_user_set=set()), provides=Users)
    provider.provide(RegisterUser[str])
    provider.provide(ViewUser[str])

    return make_async_container(provider)
