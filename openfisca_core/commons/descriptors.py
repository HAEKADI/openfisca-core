from __future__ import annotations

from typing import Any, Callable, Optional, Type

F = Callable[..., Optional[Any]]


class MethodDescriptor:
    """A generic method `descriptor`_.

    Note:
        The main idea of this module is to extract the dependency from
        :class:`.Entity`. However, it may be good also to completly deprecate
        this indirection in the future.

    Attributes:
        name (:obj:`str`): The name of the descriptor.

    Args:
        name: The name of the descriptor.

    Examples:
        >>> class Ruleset:
        ...     variable = MethodDescriptor("variable")

        >>> def get_variable(name):
        ...     # ... some logic here
        ...     if name == "this":
        ...         return "This!"

        >>> ruleset = Ruleset()
        >>> ruleset.variable
        >>> ruleset.variable = get_variable
        >>> ruleset.variable("that")
        >>> ruleset.variable("this")
        'This!'

    .. _descriptor: https://docs.python.org/3/howto/descriptor.html

    .. versionadded:: 35.7.0

    """

    public_name: str
    private_name: str

    def __init__(self, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: Type[Any]) -> Optional[F]:

        func: Optional[F] = getattr(instance, self.private_name, None)
        return func

    def __set__(self, instance: Any, value: F) -> None:

        setattr(instance, self.private_name, value)
