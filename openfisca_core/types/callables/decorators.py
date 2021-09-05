from typing import Any, Dict, List, Callable, TypeVar

ArgsType = List
A = TypeVar("A", bound = ArgsType)

KwdsType = Dict
K = TypeVar("K", bound = KwdsType)

#: Used in decorators to preserve the signature of the function it decorates
#: See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
DecoType = Callable[[ArgsType, KwdsType], Callable[[ArgsType, KwdsType], Any]]
F = TypeVar("F", bound = DecoType)
