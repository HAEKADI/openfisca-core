from typing import Any, Callable, TypeVar

#: Used in decorators to preserve the signature of the function it decorates
#: See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
Decorator = Callable[..., Any]
F = TypeVar("F", bound = Decorator)
