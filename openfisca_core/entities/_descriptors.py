from __future__ import annotations

from typing import Callable, Type, Union

from openfisca_core.types import Personifiable


class VariableDescriptor:
    public_name: str = "variable"
    private_name: str = "_variable"

    def __get__(
            self,
            instance: Personifiable,
            owner: Type[Personifiable] = None,
            ) -> Union[VariableDescriptor, Callable]:

        return getattr(instance, self.private_name, None)

    def __set__(
            self,
            instance: Personifiable,
            value: Callable,
            ) -> None:

        setattr(instance, self.private_name, value)
