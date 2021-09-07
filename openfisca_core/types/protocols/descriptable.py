from typing import Any, Callable, Optional, Type, TypeVar

from typing_extensions import Protocol

T = TypeVar("T", covariant = True)
F = Callable[..., Optional[T]]


class Descriptable(Protocol[T]):
    public_name: str
    private_name: str

    def __get__(self, obj: Any, type: Type[Any]) -> Optional[F]:
        ...

    def __set__(self, obj: Any, value: F) -> None:
        ...
