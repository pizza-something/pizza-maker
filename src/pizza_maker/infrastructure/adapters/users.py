from collections.abc import Iterator
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select

from pizza_maker.application.ports.users import Users
from pizza_maker.entities.core.user import User
from pizza_maker.infrastructure.sqlalchemy.driver import PostgresDriver
from pizza_maker.infrastructure.sqlalchemy.tables import user_table


@dataclass(kw_only=True, frozen=True, slots=True, unsafe_hash=False)
class InMemoryUsers(Users):
    _user_set: set[User]

    def __iter__(self) -> Iterator[User]:
        return iter(set(self._user_set))

    def __bool__(self) -> bool:
        return bool(self._user_set)

    async def user_with_id(self, id: UUID) -> User | None:
        for user in self._user_set:
            if user.id == id:
                return user

        return None


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresUsers(Users, PostgresDriver):
    async def user_with_id(self, id: UUID) -> User | None:
        stmt = select(User).where(user_table.c.id == id)

        return await self.session.scalar(stmt)
