from typing import Optional, Callable, Type

from openfisca_core.types import Personifiable


class VariableDescriptor:

    def __init__(self, name):
        self.name = name

    def __call__(self, entity):
        setattr(entity, self.name, self)
        return entity

    def __get__(
            self,
            entity: Personifiable,
            entity_type: Type[Personifiable] = None,
            ) -> Optional[Callable]:

        if entity is None:
            return self

        return getattr(entity, f"_{self.name}", None)

    def __set__(
            self,
            entity: Personifiable,
            get_variable: Callable,
            ) -> None:

        if self.name is "tax_benefit_system":
            setattr(entity, f"_{self.name}", get_variable)
            setattr(entity, "_get_variable", get_variable.get_variable)
