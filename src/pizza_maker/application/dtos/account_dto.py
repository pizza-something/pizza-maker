from dataclasses import dataclass
from uuid import UUID

from pizza_maker.entities.access.account import Account


@dataclass(kw_only=True, frozen=True, slots=True)
class AccountDto:
    id: UUID


def input_account_of(dto: AccountDto) -> Account:
    return Account(id=dto.id)
