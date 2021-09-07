import abc
from typing import Any, Iterable, TypeVar

from typing_extensions import Protocol

_T = TypeVar("_T", covariant = True)


class Instantizable(Iterable[_T], Protocol):

    @abc.abstractmethod
    def __getitem__(self, key: Any) -> _T:
        ...
