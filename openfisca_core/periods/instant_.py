import calendar
import datetime

from openfisca_core import periods


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

        """

        return f"{self.__class__.__name__}({super().__repr__()})"

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

        """

        instant_str = periods.STR_BY_INSTANT_CACHE.get(self)

        if instant_str is None:
            periods.STR_BY_INSTANT_CACHE[self] = instant_str = self.date.isoformat()

        return instant_str

    @property
    def date(self) -> datetime.time:
        """Converts instant to a date.

        Returns:
            :obj:`datetime.date`: The converted :obj:`.Instant`.

        Examples:
            >>> Instant((2021, 9, 13)).date
            datetime.date(2021, 9, 13)

        """

        instant_date = periods.DATE_BY_INSTANT_CACHE.get(self)

        if instant_date is None:
            periods.DATE_BY_INSTANT_CACHE[self] = instant_date = datetime.date(*self)

        return instant_date

    @property
    def year(self) -> int:
        """Extracts year from :obj:`.Instant`.

        Returns:
            int: The ``year``.

        Examples:
            >>> Instant((2021, 9, 13)).month
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

    def period(self, unit, size = 1):
        """
        Create a new period starting at instant.

        >>> instant(2014).period('month')
        Period(('month', Instant((2014, 1, 1)), 1))
        >>> instant('2014-2').period('year', 2)
        Period(('year', Instant((2014, 2, 1)), 2))
        >>> instant('2014-2-3').period('day', size = 2)
        Period(('day', Instant((2014, 2, 3)), 2))
        """
        assert unit in (periods.DAY, periods.MONTH, periods.YEAR), 'Invalid unit: {} of type {}'.format(unit, type(unit))
        assert isinstance(size, int) and size >= 1, 'Invalid size: {} of type {}'.format(size, type(size))
        return periods.Period((unit, self, size))

    def offset(self, offset, unit):
        """
        Increment (or decrement) the given instant with offset units.

        >>> instant(2014).offset(1, 'day')
        Instant((2014, 1, 2))
        >>> instant(2014).offset(1, 'month')
        Instant((2014, 2, 1))
        >>> instant(2014).offset(1, 'year')
        Instant((2015, 1, 1))

        >>> instant('2014-1-31').offset(1, 'day')
        Instant((2014, 2, 1))
        >>> instant('2014-1-31').offset(1, 'month')
        Instant((2014, 2, 28))
        >>> instant('2014-1-31').offset(1, 'year')
        Instant((2015, 1, 31))

        >>> instant('2011-2-28').offset(1, 'day')
        Instant((2011, 3, 1))
        >>> instant('2011-2-28').offset(1, 'month')
        Instant((2011, 3, 28))
        >>> instant('2012-2-29').offset(1, 'year')
        Instant((2013, 2, 28))

        >>> instant(2014).offset(-1, 'day')
        Instant((2013, 12, 31))
        >>> instant(2014).offset(-1, 'month')
        Instant((2013, 12, 1))
        >>> instant(2014).offset(-1, 'year')
        Instant((2013, 1, 1))

        >>> instant('2011-3-1').offset(-1, 'day')
        Instant((2011, 2, 28))
        >>> instant('2011-3-31').offset(-1, 'month')
        Instant((2011, 2, 28))
        >>> instant('2012-2-29').offset(-1, 'year')
        Instant((2011, 2, 28))

        >>> instant('2014-1-30').offset(3, 'day')
        Instant((2014, 2, 2))
        >>> instant('2014-10-2').offset(3, 'month')
        Instant((2015, 1, 2))
        >>> instant('2014-1-1').offset(3, 'year')
        Instant((2017, 1, 1))

        >>> instant(2014).offset(-3, 'day')
        Instant((2013, 12, 29))
        >>> instant(2014).offset(-3, 'month')
        Instant((2013, 10, 1))
        >>> instant(2014).offset(-3, 'year')
        Instant((2011, 1, 1))

        >>> instant(2014).offset('first-of', 'month')
        Instant((2014, 1, 1))
        >>> instant('2014-2').offset('first-of', 'month')
        Instant((2014, 2, 1))
        >>> instant('2014-2-3').offset('first-of', 'month')
        Instant((2014, 2, 1))

        >>> instant(2014).offset('first-of', 'year')
        Instant((2014, 1, 1))
        >>> instant('2014-2').offset('first-of', 'year')
        Instant((2014, 1, 1))
        >>> instant('2014-2-3').offset('first-of', 'year')
        Instant((2014, 1, 1))

        >>> instant(2014).offset('last-of', 'month')
        Instant((2014, 1, 31))
        >>> instant('2014-2').offset('last-of', 'month')
        Instant((2014, 2, 28))
        >>> instant('2012-2-3').offset('last-of', 'month')
        Instant((2012, 2, 29))

        >>> instant(2014).offset('last-of', 'year')
        Instant((2014, 12, 31))
        >>> instant('2014-2').offset('last-of', 'year')
        Instant((2014, 12, 31))
        >>> instant('2014-2-3').offset('last-of', 'year')
        Instant((2014, 12, 31))
        """
        year, month, day = self
        assert unit in (periods.DAY, periods.MONTH, periods.YEAR), 'Invalid unit: {} of type {}'.format(unit, type(unit))
        if offset == 'first-of':
            if unit == periods.MONTH:
                day = 1
            elif unit == periods.YEAR:
                month = 1
                day = 1
        elif offset == 'last-of':
            if unit == periods.MONTH:
                day = calendar.monthrange(year, month)[1]
            elif unit == periods.YEAR:
                month = 12
                day = 31
        else:
            assert isinstance(offset, int), 'Invalid offset: {} of type {}'.format(offset, type(offset))
            if unit == periods.DAY:
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
            elif unit == periods.MONTH:
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
            elif unit == periods.YEAR:
                year += offset
                # Handle february month of leap year.
                month_last_day = calendar.monthrange(year, month)[1]
                if day > month_last_day:
                    day = month_last_day

        return self.__class__((year, month, day))
