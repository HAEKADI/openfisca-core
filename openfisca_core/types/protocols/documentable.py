from typing_extensions import Protocol

from .dedentable import Dedentable


class Documentable(Dedentable, Protocol):
    key: str
    plural: str
    label: str
    doc: str
