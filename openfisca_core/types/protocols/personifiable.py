import typing_extensions
from typing_extensions import Protocol

from .descriptable import Descriptable
from .documentable import Documentable


@typing_extensions.runtime_checkable
class Personifiable(Documentable, Protocol):
    key: str
    plural: str
    label: str
    doc: str
    is_person: bool
    variable: Descriptable
