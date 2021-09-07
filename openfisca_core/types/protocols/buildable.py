from __future__ import annotations

import abc
from typing import Iterable, Sequence, Type, TypeVar

from typing_extensions import Protocol

BuilderType = TypeVar("BuilderType", covariant = True)
BuildeeType = TypeVar("BuildeeType", covariant = True)
BuildeeLike = TypeVar("BuildeeLike", contravariant = True)


class Buildable(Protocol[BuilderType, BuildeeType, BuildeeLike]):

    @abc.abstractmethod
    def __init__(
            self,
            builder: BuilderType,
            buildee: Type[BuildeeType],
            ) -> None:
        ...

    @abc.abstractmethod
    def __call__(self, items: Iterable[BuildeeLike]) -> Sequence[BuildeeType]:
        ...

    @abc.abstractmethod
    def build(self, item: BuildeeLike) -> BuildeeType:
        ...
