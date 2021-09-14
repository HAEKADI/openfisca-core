from __future__ import annotations

import enum
import typing
from typing import Any, Dict, Iterable, Tuple, TypeVar

from openfisca_core.indexed_enums import Enum

T = TypeVar("T", bound = "Unit")


class UnitMeta(enum.EnumMeta):

    @typing.overload
    def __contains__(self, member: str) -> bool:
        ...

    @typing.overload
    def __contains__(self, member: T) -> bool:
        ...

    @typing.overload
    def __contains__(self, member: Any) -> bool:
        ...

    def __contains__(self, member):

        if isinstance(member, str):
            return member.lower() in self.keys()

        return super().__contains__(member)

    @typing.overload
    def __getitem__(self, name: str) -> T:
        ...

    @typing.overload
    def __getitem__(self, name: T) -> T:
        ...

    @typing.overload
    def __getitem__(self, name: Any) -> T:
        ...

    def __getitem__(self, name):

        if isinstance(name, str):
            return self._member_map_[name.capitalize()]

        if isinstance(name, self):
            return self._member_map_[name.key.capitalize()]

        return super().__getitem__(name)


class Unit(Enum, metaclass = UnitMeta):
    """The date units of a rule system.

    Attributes:
        index (:obj:`int`): The ``index`` of each item.
        name (:obj:`str`): The ``name`` of each item.
        key (:obj:`str`): A unique ``key`` to identify each item.
        weight (:obj:`int`): ?
        value (tuple(str, int)): The ``key`` and ``weighr`` of each item.

    Examples:
        >>> Unit
        <enum 'Unit'>

        >>> list(Unit)
        [<Unit.Day: ('day', 100)>, ...]

        >>> len(Unit)
        4

        >>> Unit.Day
        <Unit.Day: ('day', 100)>

        >>> str(Unit.Day)
        'day'

        >>> Unit["DAY"]
        <Unit.Day: ('day', 100)>

        >>> Unit["Day"]
        <Unit.Day: ('day', 100)>

        >>> Unit["day"]
        <Unit.Day: ('day', 100)>

        >>> Unit(('day', 100))
        <Unit.Day: ('day', 100)>

        >>> Unit[Unit.Day]
        <Unit.Day: ('day', 100)>

        >>> Unit.Day.index
        0

        >>> Unit.Day.name
        'Day'

        >>> Unit.Day.value
        ('day', 100)

        >>> Unit.Day.key
        'day'

        >>> Unit.Day.weight
        100

        >>> Unit.Day in Unit
        True

        >>> Unit.Day not in Unit
        False

        >>> "DAY" in Unit
        True

        >>> "DAY" not in Unit
        False

        >>> "Day" in Unit
        True

        >>> "Day" not in Unit
        False

        >>> "day" in Unit
        True

        >>> "day" not in Unit
        False

        >>> Unit.Day == Unit.Day
        True

        >>> Unit.Day != Unit.Day
        False

        >>> "DAY" == Unit.Day
        True

        >>> "DAY" != Unit.Day
        False

        >>> "Day" == Unit.Day
        True

        >>> "Day" != Unit.Day
        False

        >>> "day" == Unit.Day
        True

        >>> "day" != Unit.Day
        False

        >>> Unit.Day < Unit.Month
        True

        >>> Unit.Day > Unit.Month
        False

        >>> Unit.Day < Unit.Day
        False

        >>> Unit.Day > Unit.Day
        False

        >>> "DAY" < Unit.Month
        True

        >>> "DAY" > Unit.Month
        False

        >>> "DAY" < Unit.Day
        False

        >>> "DAY" > Unit.Day
        False

        >>> "Day" < Unit.Month
        True

        >>> "Day" > Unit.Month
        False

        >>> "Day" < Unit.Day
        False

        >>> "Day" > Unit.Day
        False

        >>> "day" < Unit.Month
        True

        >>> "day" > Unit.Month
        False

        >>> "day" < Unit.Day
        False

        >>> "day" > Unit.Day
        False

    .. versionadded:: 35.9.0

    """

    # Attributes

    index: int
    name: str
    key: str
    weight: int
    value: Tuple[str, int]

    # Members

    Day = ("day", 100)
    Month = ("month", 200)
    Year = ("year", 300)
    Eternity = ("eternity", 400)

    def __str__(self) -> str:
        return self.key

    def __hash__(self) -> int:

        return hash(self.key)

    @typing.overload
    def __eq__(self, value: str) -> bool:
        ...

    @typing.overload
    def __eq__(self, value: Any) -> bool:
        ...

    def __eq__(self, value) -> bool:

        if isinstance(value, str):
            return self.key == value.lower()

        return super().__eq__(value)

    @typing.overload
    def __lt__(self, value: str) -> bool:
        ...

    @typing.overload
    def __lt__(self, value: T) -> bool:
        ...

    @typing.overload
    def __lt__(self, value: Any) -> bool:
        ...

    def __lt__(self, value) -> bool:

        if isinstance(value, str):
            return self.weight < self._member_map_[value.capitalize()].weight

        if isinstance(value, self.__class__):
            return self.weight < value.weight

        return super().__lt__(value)

    @typing.overload
    def __gt__(self, value: str) -> bool:
        ...

    @typing.overload
    def __gt__(self, value: T) -> bool:
        ...

    @typing.overload
    def __gt__(self, value: Any) -> bool:
        ...

    def __gt__(self, value) -> bool:

        if isinstance(value, str):
            return self._member_map_[value.capitalize()].__lt__(self)

        if isinstance(value, self.__class__):
            return value.__lt__(self)

        return super().__gt__(value)

    def __init__(self, name: str, weight: int) -> None:

        super().__init__(name)
        self.key = name
        self.weight = weight

    @classmethod
    def keys(cls: Iterable[T]) -> Tuple[str, ...]:
        """Creates a :obj:`tuple` of ``key`` with each item.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> Unit.keys()
            ('day', 'month', 'year', 'eternity')

        """

        return tuple(item.key for item in cls)

    @classmethod
    def ethereal(cls: Iterable[T]) -> Tuple[str, ...]:
        """Creates a :obj:`tuple` of ``key`` with ethereal items.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> Unit.ethereal()
            ('day', 'month', 'year')

        """

        return tuple(item.key for item in cls if item != Unit.Eternity)

    @classmethod
    def eternal(cls: Iterable[T]) -> Tuple[str, ...]:
        """Creates a :obj:`tuple` of ``key`` with eternal items.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> Unit.eternal()
            ('eternity',)

        """

        return tuple(item.key for item in cls if item == Unit.Eternity)

    @classmethod
    def weights(cls: Iterable[T]) -> Dict[str, int]:
        """Creates a :obj:`dict` of ``weight`` with each item.

        Returns:
            dict(str, int): A :obj:`dict` mapping [``key``, ``weight``].

        Examples:
            >>> Unit.weights()
            {'day': 100, 'month': 200, 'year': 300, 'eternity': 400}

        """

        return {item.key: item.weight for item in cls}

    def upper(self) -> str:
        """Uppercases the :class:`.Unit`.

        Returns:
            :obj:`str`: The uppercased :class:`.Unit`.

        Examples:
            >>> Unit.Day.upper()
            'DAY'

        """

        return self.key.upper()

    def lower(self) -> str:
        """Lowecases the :class:`.Unit`.

        Returns:
            :obj:`str`: The lowercased :class:`.Unit`.

        Examples:
            >>> Unit.Day.lower()
            'day'

        """

        return self.key.lower()
