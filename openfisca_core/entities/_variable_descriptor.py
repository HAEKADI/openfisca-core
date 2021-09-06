from typing import Optional, Callable, Type

from openfisca_core.types import Personifiable


class VariableDescriptor:

    def __get__(
            self,
            entity: Personifiable,
            entity_type: Type[Personifiable] = None,
            ) -> Optional[Callable]:

        if entity is None:
            return None

        return getattr(entity, "_get_variable", None)

    def __set__(
            self,
            entity: Personifiable,
            get_variable: Callable,
            ) -> None:

        entity._get_variable = get_variable
