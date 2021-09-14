from __future__ import annotations

import datetime
import os
import typing
from typing import Dict, Optional, Union

from openfisca_core import commons, periods

from .unit import Unit


def N_(message):
    return message


def instant(instant):
    """Return a new instant, aka a triple of integers (year, month, day).

    >>> instant(2014)
    Instant((2014, 1, 1))
    >>> instant('2014')
    Instant((2014, 1, 1))
    >>> instant('2014-02')
    Instant((2014, 2, 1))
    >>> instant('2014-03-02')
    Instant((2014, 3, 2))
    >>> instant(instant('2014-03-02'))
    Instant((2014, 3, 2))
    >>> instant(period('month:2014-3-2'))
    Instant((2014, 3, 2))

    >>> instant(None)
    """
    if instant is None:
        return None
    if isinstance(instant, periods.Instant):
        return instant
    if isinstance(instant, str):
        if not periods.INSTANT_PATTERN.match(instant):
            raise ValueError("'{}' is not a valid instant. Instants are described using the 'YYYY-MM-DD' format, for instance '2015-06-15'.".format(instant))
        instant = periods.Instant(
            int(fragment)
            for fragment in instant.split('-', 2)[:3]
            )
    elif isinstance(instant, datetime.date):
        instant = periods.Instant((instant.year, instant.month, instant.day))
    elif isinstance(instant, int):
        instant = (instant,)
    elif isinstance(instant, list):
        assert 1 <= len(instant) <= 3
        instant = tuple(instant)
    elif isinstance(instant, periods.Period):
        instant = instant.start
    else:
        assert isinstance(instant, tuple), instant
        assert 1 <= len(instant) <= 3
    if len(instant) == 1:
        return periods.Instant((instant[0], 1, 1))
    if len(instant) == 2:
        return periods.Instant((instant[0], instant[1], 1))
    return periods.Instant(instant)


def instant_date(instant):
    if instant is None:
        return None
    instant_date = periods.DATE_BY_INSTANT_CACHE.get(instant)
    if instant_date is None:
        periods.DATE_BY_INSTANT_CACHE[instant] = instant_date = datetime.date(*instant)
    return instant_date


def period(value):
    """Return a new period, aka a triple (unit, start_instant, size).

    >>> period('2014')
    Period((<Unit.Year: ('year', 300)>, Instant((2014, 1, 1)), 1))
    >>> period('year:2014')
    Period(('year', Instant((2014, 1, 1)), 1))

    >>> period('2014-2')
    Period((<Unit.Month: ('month', 200)>, Instant((2014, 2, 1)), 1))
    >>> period('2014-02')
    Period((<Unit.Month: ('month', 200)>, Instant((2014, 2, 1)), 1))
    >>> period('month:2014-2')
    Period(('month', Instant((2014, 2, 1)), 1))

    >>> period('year:2014-2')
    Period(('year', Instant((2014, 2, 1)), 1))
    """
    if isinstance(value, periods.Period):
        return value

    if isinstance(value, periods.Instant):
        return periods.Period((Unit.Day, value, 1))

    def parse_simple_period(value):
        """
        Parses simple periods respecting the ISO format, such as 2012 or 2015-03
        """
        try:
            date = datetime.datetime.strptime(value, '%Y')
        except ValueError:
            try:
                date = datetime.datetime.strptime(value, '%Y-%m')
            except ValueError:
                try:
                    date = datetime.datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    return None
                else:
                    return periods.Period((Unit.Day, periods.Instant((date.year, date.month, date.day)), 1))
            else:
                return periods.Period((Unit.Month, periods.Instant((date.year, date.month, 1)), 1))
        else:
            return periods.Period((Unit.Year, periods.Instant((date.year, date.month, 1)), 1))

    def raise_error(value):
        message = os.linesep.join([
            "Expected a period (eg. '2017', '2017-01', '2017-01-01', ...); got: '{}'.".format(value),
            "Learn more about legal period formats in OpenFisca:",
            "<https://openfisca.org/doc/coding-the-legislation/35_periods.html#periods-in-simulations>."
            ])
        raise ValueError(message)

    if value == 'ETERNITY' or value == Unit.Eternity:
        return periods.Period(('eternity', instant(datetime.date.min), float("inf")))

    # check the type
    if isinstance(value, int):
        return periods.Period((Unit.Year, periods.Instant((value, 1, 1)), 1))
    if not isinstance(value, str):
        raise_error(value)

    # try to parse as a simple period
    period = parse_simple_period(value)
    if period is not None:
        return period

    # complex period must have a ':' in their strings
    if ":" not in value:
        raise_error(value)

    components = value.split(':')

    # left-most component must be a valid unit
    unit = components[0]

    if unit not in Unit.ethereal():
        raise_error(value)

    # middle component must be a valid iso period
    base_period = parse_simple_period(components[1])
    if not base_period:
        raise_error(value)

    # period like year:2015-03 have a size of 1
    if len(components) == 2:
        size = 1
    # if provided, make sure the size is an integer
    elif len(components) == 3:
        try:
            size = int(components[2])
        except ValueError:
            raise_error(value)
    # if there is more than 2 ":" in the string, the period is invalid
    else:
        raise_error(value)

    # reject ambiguous period such as month:2014
    if base_period.unit > unit:
        raise_error(value)

    return periods.Period((unit, base_period.start, size))


def key_period_size(period: periods.Period) -> str:
    """Defines a key in order to sort periods by length.

    It uses two aspects: first, ``unit``, then, ``size``.

    Args:
        period: An :mod:`.openfisca_core` :obj:`.Period`.

    Returns:
        :obj:`str`: A string.

    Examples:
        >>> instant = periods.Instant((2021, 9, 14))

        >>> period = periods.Period((Unit.Day, instant, 1))
        >>> key_period_size(period)
        '100_1'

        >>> period = periods.Period(("month", instant, 2))
        >>> key_period_size(period)
        '200_2'

        >>> period = periods.Period(("Year", instant, 3))
        >>> key_period_size(period)
        '300_3'

        >>> period = periods.Period(("ETERNITY", instant, 4))
        >>> key_period_size(period)
        '400_4'

    .. versionchanged:: 35.9.0
        Hereafter uses :attr:`.Unit.weight`.

    """

    unit: Union[Unit, str]
    size: int

    unit, _, size = period

    if isinstance(unit, str):
        unit = Unit[unit]

    return f"{unit.weight}_{size}"


@commons.deprecated(since = "35.9.0", expires = "the future")
def unit_weights() -> Dict[str, int]:
    """Finds the weight of each date unit.

    Returns:
        dict(str, int): A dictionary with the corresponding values.

    Examples:
        >>> unit_weights()
        {'day': 100, 'month': 200, 'year': 300, 'eternity': 400}

    .. deprecated:: 35.9.0
        :func:`.unit_weights` has been deprecated and will be
        removed in the future. The functionality is now provided by
        :func:`.Unit.weights`.

    """

    return Unit.weights()


@typing.overload
def unit_weight(unit: str) -> Optional[int]:
    ...


@typing.overload
def unit_weight(unit: Unit) -> Optional[int]:
    ...


@commons.deprecated(since = "35.9.0", expires = "the future")
def unit_weight(unit):
    """Finds the weight of a specific date unit.

    Args:
        unit: The unit to find the weight for.

    Returns:
        int: The weight.

    Examples:
        >>> unit_weight(Unit.Day)
        100

        >>> unit_weight('DAY')
        100

        >>> unit_weight('Day')
        100

        >>> unit_weight('day')
        100

    .. deprecated:: 35.9.0
        :func:`.unit_weight` has been deprecated and will be
        removed in the future. The functionality is now provided by
        :attr:`.Unit.weight`.

    """

    if isinstance(unit, str):
        unit = Unit[unit]

    return unit.weight
