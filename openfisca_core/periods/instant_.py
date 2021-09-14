from __future__ import annotations

import calendar
import datetime
import functools

from openfisca_core import periods
from openfisca_core.types import EtherealLike

from .unit import Unit


class Instant(tuple):
    """An instant in time (year, month, day).

    An :class:`.Instant` represents the most atomic and indivisible unit time
    of a legislations.

    Current implementation considers this unit to be a day, so
    :obj:`instants <.Instant>` can be thought of as "day dates".

    Args:
        iterable (tuple(int, int, int)):
            The ``year``, ``month``, and ``day``, accordingly.

    Examples:
        >>> instant = Instant((2021, 9, 13))
        >>> instant
        Instant((2021, 9, 13))

        >>> instant.year
        2021

        >>> instant.month
        9

        >>> instant.day
        13

    """

    @functools.lru_cache(maxsize = None)
    def __repr__(self) -> str:
        """Casts an :obj:`.Instant` to its "official" :obj:`str` form.

        :meth:`.repr` is mainly used for debugging and development, and its
        goal is to be unambiguous. :meth:`.repr` computes the "official"
        :obj:`str` representation of an :obj:`.Instant`.

        Returns:
            :obj:`str`: The "official" string representation of an
            :obj:`.Instant`.

        Examples:
            >>> repr(Instant((2021, 9, 13)))
            'Instant((2021, 9, 13))'

            >>> repr(Instant((2021, 9, 14)))
            'Instant((2021, 9, 14))'

        """

        return f"{self.__class__.__name__}({super().__repr__()})"

    @functools.lru_cache(maxsize = None)
    def __str__(self) -> str:
        """Casts an :obj:`.Instant` to its "unofficial" :obj:`str` form.

        :meth:`.str` is mainly used for creating output for end user, and its
        goal is to be readable. :meth:`.str` :meth:`.repr` computes the
        "unofficial" :obj:`str` representation of an :obj:`.Instant`.

        Returns:
            :obj:`str`: The "unofficial" string representation of an
            :obj:`.Instant`.

        Examples:
            >>> str(Instant((2021, 9, 13)))
            '2021-09-13'

            >>> str(Instant((2021, 9, 14)))
            '2021-09-14'

        """

        return self.date.isoformat()

    @property
    def date(self) -> datetime.date:
        """Converts instant to a date.

        Returns:
            :obj:`datetime.date`: The converted :obj:`.Instant`.

        Examples:
            >>> Instant((2021, 9, 13)).date
            datetime.date(2021, 9, 13)

            >>> Instant((2021, 9, 14)).date
            datetime.date(2021, 9, 14)

        """

        decorator = functools.lru_cache(maxsize = None)
        return decorator(datetime.date)(*self)

    @property
    def year(self) -> int:
        """Extracts year from :obj:`.Instant`.

        Returns:
            int: The ``year``.

        Examples:
            >>> Instant((2021, 9, 13)).year
            2021

        """

        return self[0]

    @property
    def month(self) -> int:
        """Extracts month from :obj:`.Instant`.

        Returns:
            int: The ``month``.

        Examples:
            >>> Instant((2021, 9, 13)).month
            9

        """

        return self[1]

    @property
    def day(self) -> int:
        """Extracts day from :obj:`.Instant`.

        Returns:
            int: The ``day``.

        Examples:
            >>> Instant((2021, 9, 13)).day
            13

        """

        return self[2]

    def period(self, unit: EtherealLike, size: int = 1) -> periods.Period:
        """Creates a new :obj:`.Period` starting at :obj:`.Instant`.

        Todo:
            * Somehow remove cyclic dependency.
            * Fix signature (why dont literal work with enums ...0.

        Args:
            unit: ``day`` or ``month`` or ``year``.
            size: How many of ``unit``.

        Returns:
            A new object :obj:`.Period`.

        Examples:
            >>> Instant((2021, 9, 13)).period(Unit.Year)
            Period((Unit.Year(('year', 300)), Instant((2021, 9, 13)), 1))

            >>> Instant((2021, 9, 13)).period(Unit.Month, 2)
            Period((Unit.Month(('month', 200)), Instant((2021, 9, 13)), 2))

            >>> Instant((2021, 9, 13)).period(Unit.Day, 1000)
            Period((Unit.Day(('day', 100)), Instant((2021, 9, 13)), 1000))

        """

        assert unit in Unit, \
            f"Invalid unit: {unit} of type {type(unit)}. Expecting any of " \
            f"{', '.join(str(unit) for unit in Unit)}."

        assert isinstance(size, int) and size >= 1, \
            f"Invalid size: {size} of type {type(size)}"

        return periods.Period((unit, self, size))

    def offset(self, offset, unit):
        """
        Increment (or decrement) the given instant with offset units.

        Todo:
            * split in factories, or functions, etc.


        >>> Instant((2021, 1, 1)).offset(1, 'day')
        Instant((2021, 1, 2))
        >>> Instant((2021, 1, 1)).offset(1, 'month')
        Instant((2021, 2, 1))
        >>> Instant((2021, 1, 1)).offset(1, 'year')
        Instant((2022, 1, 1))

        >>> Instant((2021, 1, 31)).offset(1, 'day')
        Instant((2021, 2, 1))
        >>> Instant((2021, 1, 31)).offset(1, 'month')
        Instant((2021, 2, 28))
        >>> Instant((2021, 1, 31)).offset(1, 'year')
        Instant((2022, 1, 31))

        >>> Instant((2011, 2, 28)).offset(1, 'day')
        Instant((2011, 3, 1))
        >>> Instant((2011, 2, 28)).offset(1, 'month')
        Instant((2011, 3, 28))
        >>> Instant((2012, 2, 29)).offset(1, 'year')
        Instant((2013, 2, 28))

        >>> Instant((2021, 1, 1)).offset(-1, 'day')
        Instant((2020, 12, 31))
        >>> Instant((2021, 1, 1)).offset(-1, 'month')
        Instant((2020, 12, 1))
        >>> Instant((2021, 1, 1)).offset(-1, 'year')
        Instant((2020, 1, 1))

        >>> Instant((2011, 3, 1)).offset(-1, 'day')
        Instant((2011, 2, 28))
        >>> Instant((2011, 3, 31)).offset(-1, 'month')
        Instant((2011, 2, 28))
        >>> Instant((2012, 2, 29)).offset(-1, 'year')
        Instant((2011, 2, 28))

        >>> Instant((2021, 1, 30)).offset(3, 'day')
        Instant((2021, 2, 2))
        >>> Instant((2021, 10, 2)).offset(3, 'month')
        Instant((2022, 1, 2))
        >>> Instant((2021, 1, 1)).offset(3, 'year')
        Instant((2024, 1, 1))

        >>> Instant((2021, 1, 1)).offset(-3, 'day')
        Instant((2020, 12, 29))
        >>> Instant((2021, 1, 1)).offset(-3, 'month')
        Instant((2020, 10, 1))
        >>> Instant((2021, 1, 1)).offset(-3, 'year')
        Instant((2018, 1, 1))

        >>> Instant((2021, 1, 1)).offset('first-of', 'month')
        Instant((2021, 1, 1))
        >>> Instant((2021, 2, 1)).offset('first-of', 'month')
        Instant((2021, 2, 1))
        >>> Instant((2021, 2, 3)).offset('first-of', 'month')
        Instant((2021, 2, 1))

        >>> Instant((2021, 1, 1)).offset('first-of', 'year')
        Instant((2021, 1, 1))
        >>> Instant((2021, 2, 1)).offset('first-of', 'year')
        Instant((2021, 1, 1))
        >>> Instant((2021, 2, 3)).offset('first-of', 'year')
        Instant((2021, 1, 1))

        >>> Instant((2021, 1, 1)).offset('last-of', 'month')
        Instant((2021, 1, 31))
        >>> Instant((2021, 2, 1)).offset('last-of', 'month')
        Instant((2021, 2, 28))
        >>> Instant((2012, 2, 3)).offset('last-of', 'month')
        Instant((2012, 2, 29))

        >>> Instant((2021, 1, 1)).offset('last-of', 'year')
        Instant((2021, 12, 31))
        >>> Instant((2021, 2, 1)).offset('last-of', 'year')
        Instant((2021, 12, 31))
        >>> Instant((2021, 2, 3)).offset('last-of', 'year')
        Instant((2021, 12, 31))

        """

        year, month, day = self
        assert unit in Unit.ethereal(), 'Invalid unit: {} of type {}'.format(unit, type(unit))
        if offset == 'first-of':
            if unit == Unit.Month:
                day = 1
            elif unit == Unit.Year:
                month = 1
                day = 1
        elif offset == 'last-of':
            if unit == Unit.Month:
                day = calendar.monthrange(year, month)[1]
            elif unit == Unit.Year:
                month = 12
                day = 31
        else:
            assert isinstance(offset, int), 'Invalid offset: {} of type {}'.format(offset, type(offset))
            if unit == Unit.Day:
                day += offset
                if offset < 0:
                    while day < 1:
                        month -= 1
                        if month == 0:
                            year -= 1
                            month = 12
                        day += calendar.monthrange(year, month)[1]
                elif offset > 0:
                    month_last_day = calendar.monthrange(year, month)[1]
                    while day > month_last_day:
                        month += 1
                        if month == 13:
                            year += 1
                            month = 1
                        day -= month_last_day
                        month_last_day = calendar.monthrange(year, month)[1]
            elif unit == Unit.Month:
                month += offset
                if offset < 0:
                    while month < 1:
                        year -= 1
                        month += 12
                elif offset > 0:
                    while month > 12:
                        year += 1
                        month -= 12
                month_last_day = calendar.monthrange(year, month)[1]
                if day > month_last_day:
                    day = month_last_day
            elif unit == Unit.Year:
                year += offset
                # Handle february month of leap year.
                month_last_day = calendar.monthrange(year, month)[1]
                if day > month_last_day:
                    day = month_last_day

        return self.__class__((year, month, day))
