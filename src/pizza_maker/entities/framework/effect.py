from dataclasses import dataclass
from itertools import chain
from typing import Any, Callable, Never, cast

from pizza_maker.entities.framework.identified import Identified, Identity


class DuplicateError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Effect[
    ValueT = None,
    NewT: Identified = Never,
    DirtyT: Identified = Never,
    DeletedT: Identified = Never,
]:
    value: ValueT
    new_values: tuple[NewT, ...]
    dirty_values: tuple[DirtyT, ...]
    deleted_values: tuple[DeletedT, ...]

    def __and__[
        OtherValueT,
        OtherNewT: Identified,
        OtherDirtyT: Identified,
        OtherDeletedT: Identified,
    ](
        self,
        other: "Effect[OtherValueT, OtherNewT, OtherDirtyT, OtherDeletedT]",
    ) -> "Effect[OtherValueT, NewT | OtherNewT, DirtyT | OtherDirtyT, DeletedT | OtherDeletedT]":  # noqa: E501
        next_new_values = (
            self._part_of_next_new_values_when(other=cast(AnyEffect, other))
            + other._part_of_next_new_values_when(other=cast(AnyEffect, self))
        )
        next_dirty_values = (
            self._part_of_next_dirty_values_when(other=cast(AnyEffect, other))
            + other._part_of_next_dirty_values_when(other=cast(AnyEffect, self))
        )
        next_deleted_values = self.deleted_values + other.deleted_values

        return Effect(
            value=other.value,
            new_values=next_new_values,
            dirty_values=next_dirty_values,
            deleted_values=next_deleted_values,
        )

    def _part_of_next_new_values_when(
        self, *, other: "AnyEffect"
    ) -> tuple[NewT, ...]:
        return tuple(
            new_value
            for new_value in self.new_values
            if not other.is_dirty(new_value) and not other.is_deleted(new_value)
        )

    def _part_of_next_dirty_values_when(
        self, *, other: "AnyEffect"
    ) -> tuple[DirtyT, ...]:
        return tuple(
            dirty_value
            for dirty_value in self.dirty_values
            if not other.is_deleted(dirty_value)
        )

    def _filtered_new_values_by(self, other: "AnyEffect") -> tuple[NewT, ...]:
        return tuple(
            new_value
            for new_value in self.new_values
            if not other.is_dirty(new_value) and not other.is_deleted(new_value)
        )

    def is_dirty(self, value: Identified) -> bool:
        return self.__is_in(self.dirty_values, value)

    def is_new(self, value: Identified) -> bool:
        return self.__is_in(self.new_values, value)

    def is_deleted(self, value: Identified) -> bool:
        return self.__is_in(self.deleted_values, value)

    def map[ResultT](self, func: Callable[[ValueT], ResultT]) -> (
        "Effect[ResultT, NewT, DirtyT, DeletedT]"
    ):
        return Effect(
            value=func(self.value),
            new_values=self.new_values,
            dirty_values=self.dirty_values,
            deleted_values=self.deleted_values,
        )

    def then[
        OtherValueT,
        OtherNewT: Identified,
        OtherDirtyT: Identified,
        OtherDeletedT: Identified,
    ](
        self,
        func: Callable[
            [ValueT],
            "Effect[OtherValueT, OtherNewT, OtherDirtyT, OtherDeletedT]",
        ],
    ) -> "Effect[OtherValueT, NewT | OtherNewT, DirtyT | OtherDirtyT, DeletedT | OtherDeletedT]":  # noqa: E501
        return self & func(self.value)

    def __has_duplicates(self) -> bool:
        all_values = (
            chain(self.new_values, self.dirty_values, self.deleted_values)
        )
        all_identities = tuple(map(Identity, all_values))
        return len(all_identities) != len(set(all_identities))

    def __post_init__(self) -> None:
        if self.__has_duplicates():
            raise DuplicateError

    def __is_in(
        self, others: tuple[Identified, ...], value: Identified
    ) -> bool:
        return any(value.is_(other) for other in others)


type AnyEffect[
    ValueT = Any,
    NewT: Identified = Any,
    DirtyT: Identified = Any,
    DeletedT: Identified = Any,
] = Effect[ValueT, NewT, DirtyT, DeletedT]

type Existing[ValueT: Identified] = Effect[ValueT, Never, Never, Never]
type New[ValueT: Identified] = Effect[ValueT, ValueT, Never, Never]
type Dirty[ValueT: Identified] = Effect[ValueT, Never, ValueT, Never]
type Deleted[ValueT: Identified] = Effect[ValueT, Never, Never, ValueT]


def just[ValueT](effect: Effect[ValueT, Any, Any, Any]) -> ValueT:
    return effect.value


def existing[ValueT: Identified](value: ValueT) -> Existing[ValueT]:
    return Effect(
        value=value,
        new_values=tuple(),
        dirty_values=tuple(),
        deleted_values=tuple(),
    )


def new[ValueT: Identified](value: ValueT) -> New[ValueT]:
    return Effect(
        value=value,
        new_values=(value, ),
        dirty_values=tuple(),
        deleted_values=tuple(),
    )


def dirty[ValueT: Identified](value: ValueT) -> Dirty[ValueT]:
    return Effect(
        value=value,
        new_values=tuple(),
        dirty_values=(value, ),
        deleted_values=tuple(),
    )


def deleted[ValueT: Identified](value: ValueT) -> Deleted[ValueT]:
    return Effect(
        value=value,
        new_values=tuple(),
        dirty_values=tuple(),
        deleted_values=(value, ),
    )
