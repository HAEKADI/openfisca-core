from typing import Any, Callable, TypeVar

#: Used in decorators to preserve the signature of the function it decorates
#: See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
DecoType = Callable[..., Any]

FuncType = TypeVar("FuncType", bound = DecoType)
