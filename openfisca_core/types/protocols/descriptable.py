from typing import Any, Callable, Optional, Type, TypeVar

from typing_extensions import Protocol

_T = TypeVar("_T")
_F = Callable[..., Optional[_T]]


class Descriptable(Protocol[_T]):
    public_name: str
    private_name: str

    def __get__(self, obj: Any, type: Type[Any]) -> Optional[_F[_T]]:
        ...

    def __set__(self, obj: Any, value: _F[_T]) -> None:
        ...
