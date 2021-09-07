import abc
from typing import Iterable

from typing_extensions import Protocol


class Instantizable(Iterable, Protocol):

    @abc.abstractmethod
    def __getitem__(self, key):
        ...
