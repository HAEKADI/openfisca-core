import abc
from typing import Any, Type, TypeVar

from typing_extensions import Protocol

DescType = TypeVar("DescType", contravariant = True)


class Descriptable(Protocol[DescType]):
    public_name: str
    private_name: str

    @abc.abstractmethod
    def __get__(self, instance: DescType, owner: Type[DescType] = None) -> Any:
        ...

    @abc.abstractmethod
    def __set__(self, instance: DescType, value: Any) -> None:
        ...
