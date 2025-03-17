from contextlib import suppress
from dataclasses import dataclass

from pizza_maker.application.dtos.account_dto import (
    AccountDto,
    input_account_of,
)
from pizza_maker.application.ports.map import MapTo
from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.application.ports.users import Users
from pizza_maker.entities.core.user import (
    RegisteredUserForUserRegistrationError,
    User,
    registered_user_when,
)
from pizza_maker.entities.framework.effect import New


@dataclass(kw_only=True, frozen=True, slots=True)
class OnAccountCreated[UsersT: Users]:
    users: UsersT
    map_to: MapTo[tuple[UsersT], New[User]]
    transaction_of: TransactionOf[tuple[UsersT]]

    async def __call__(self, account_dto: AccountDto) -> None:
        account = input_account_of(account_dto)

        with suppress(RegisteredUserForUserRegistrationError):
            async with self.transaction_of((self.users, )):
                user = await self.users.user_with_id(account.id)
                user = registered_user_when(user=user, account=account)

                await self.map_to((self.users, ), user)
