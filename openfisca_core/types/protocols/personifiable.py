import abc
from typing import Any, ClassVar, Optional

import typing_extensions
from typing_extensions import Protocol

from ._documentable import Documentable
from .descriptable import Descriptable
from .modelable import Modelable
from .representable import Representable


@typing_extensions.runtime_checkable
class Personifiable(Documentable, Protocol):
    """Base type for any entity-like model.

    Type-checking against abstractions rather than implementations helps in
    (a) decoupling the codebse, thanks to structural subtyping, and
    (b) documenting/enforcing the blueprints of the different OpenFisca models.

    .. versionadded:: 35.7.0

    """

    key: str
    plural: str
    label: str
    doc: str
    is_person: ClassVar[bool]
    variable: Descriptable[Modelable]

    @abc.abstractmethod
    def __repr__(self) -> str:
        ...

    @abc.abstractmethod
    def set_tax_benefit_system(
            self,
            tax_benefit_system: Representable,
            ) -> None:
        ...

    @abc.abstractstaticmethod
    def check_role_validity(role: Any) -> None:
        ...

    @abc.abstractmethod
    def get_variable(
            self,
            variable_name: str,
            check_existence: bool = False,
            ) -> Optional[Modelable]:
        ...

    @abc.abstractmethod
    def check_variable_defined_for_entity(
            self,
            variable_name: str,
            ) -> None:
        ...
