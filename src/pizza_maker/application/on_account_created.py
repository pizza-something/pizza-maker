from dataclasses import dataclass

from pizza_maker.application.dtos.account_dto import (
    AccountDto,
    input_account_of,
)
from pizza_maker.application.ports.map import MapTo
from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.application.ports.users import Users
from pizza_maker.entities.common.effect import Existing, New
from pizza_maker.entities.core.user import (
    User,
    new_user_when,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class OnAccountCreated[UsersT: Users]:
    users: UsersT
    map_to: MapTo[tuple[UsersT], New[User] | Existing[User]]
    transaction_of: TransactionOf[tuple[UsersT]]

    async def __call__(self, account_dto: AccountDto) -> None:
        account = input_account_of(account_dto)

        async with self.transaction_of((self.users, )):
            user = await self.users.user_with_id(account.id)
            user = new_user_when(user=user, account=account)

            await self.map_to((self.users, ), user)
