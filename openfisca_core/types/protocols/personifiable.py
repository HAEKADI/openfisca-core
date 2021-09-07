from typing_extensions import Protocol

from .documentable import Documentable


class Personifiable(Documentable, Protocol):
    key: str
    plural: str
    label: str
    doc: str
    is_person: bool
