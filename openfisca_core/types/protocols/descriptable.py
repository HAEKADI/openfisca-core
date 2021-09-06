import abc
from typing import Any, Type, TypeVar
from typing_extensions import Protocol

DescType = TypeVar("DescType", contravariant = True)


class Descriptable(Protocol[DescType]):

    @abc.abstractmethod
    def __get__(self, obj: DescType, type: Type[DescType] = None) -> Any:
        ...

    @abc.abstractmethod
    def __set__(self, obj: DescType, value: Any) -> None:
        ...
