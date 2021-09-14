from typing import Dict, Tuple

from openfisca_core.indexed_enums import Enum


class Unit(Enum):
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

        >>> Unit["Day"]
         <Unit.Day: ('day', 100)>

        >>> Unit(('day', 100))
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

        >>> Unit.keys()
        ('day', 'month', 'year', 'eternity')

        >>> Unit.weights()
        {'day': 100, 'month': 200, 'year': 300, 'eternity': 400}

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

    def __init__(self, name: str, weight: int) -> None:
        super().__init__(name)
        self.key = name
        self.weight = weight

    @classmethod
    def keys(cls) -> Tuple[str, ...]:
        """Creates a :obj:`tuple` of ``key`` with each item.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> Unit.keys()
            ('day', 'month', 'year', 'eternity')

        """

        return tuple(str(item.key) for item in cls.__members__.values())

    @classmethod
    def weights(cls) -> Dict[str, int]:
        """Creates a :obj:`dict` of ``weight`` with each item.

        Returns:
            dict(str, int): A :obj:`dict` mapping [``key``, ``weight``].

        Examples:
            >>> Unit.weights()
            {'day': 100, ...}

        """

        return {item.key: item.weight for item in cls.__members__.values()}
