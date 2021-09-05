import abc
from typing_extensions import Protocol

from .representable import Representable
from ._documentable import _Documentable


class Personifiable(_Documentable, Protocol):

    @abc.abstractmethod
    def set_tax_benefit_system(
            self,
            tax_benefit_system: Representable,
            ) -> None:
        ...
