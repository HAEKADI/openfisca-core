from typing import Any, Dict, List, Callable, TypeVar

Args = List
A = TypeVar("A", bound = Args)

Kwds = Dict
K = TypeVar("K", bound = Kwds)

#: Used in decorators to preserve the signature of the function it decorates
#: See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
Decorator = Callable[[Args, Kwds], Callable[[Args, Kwds], Any]]
F = TypeVar("F", bound = Decorator)
