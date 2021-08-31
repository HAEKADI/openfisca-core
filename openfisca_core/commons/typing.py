from typing import Sequence, TypeVar, Union

from nptyping import NDArray as Array

_Types = TypeVar("_Types", bool, float, int, str)
_Array = Union[Array[bool], Array[float], Array[int], Array[str]]
ArrayLike = Union[_Array, Sequence[_Types]]
""":obj:`.Generic`: Type of any castable to :class:`.ndarray`.

These include any :obj:`.ndarray` and sequences (like
:obj:`list`, :obj:`tuple`, and so on).

Examples:
    >>> ArrayLike[float]
    typing.Union[numpy.ndarray, typing.Sequence[float]]

    >>> ArrayLike[str]
    typing.Union[numpy.ndarray, typing.Sequence[str]]

Note:
    It is possible since numpy version 1.21 to specify the type of an
    array, thanks to `numpy.typing.NDArray`_:

    .. code-block:: python

        from numpy.typing import NDArray
        NDArray[numpy.float64]

    `mypy`_ provides `duck type compatibility`_, so an :obj:`int` is
    considered to be valid whenever a :obj:`float` is expected.

Todo:
    * Refactor once numpy version >= 1.21 is used.

.. _mypy:
    https://mypy.readthedocs.io/en/stable/

.. _duck type compatibility:
    https://mypy.readthedocs.io/en/stable/duck_type_compatibility.html

.. _numpy.typing.NDArray:
    https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray

"""
