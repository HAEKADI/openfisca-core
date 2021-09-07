from __future__ import annotations

from typing import Any, Callable, Optional, Type

from openfisca_core.variables import Variable

_F = Callable[[str, bool], Optional[Variable]]


class VariableDescriptor:
    public_name: str = "variable"
    private_name: str = "_variable"

    def __get__(self, obj: Any, type: Type[Any]) -> Optional[_F]:

        func: Optional[_F]
        func = getattr(obj, self.private_name, None)
        return func

    def __set__(self, obj: Any, value: _F) -> None:

        setattr(obj, self.private_name, value)
