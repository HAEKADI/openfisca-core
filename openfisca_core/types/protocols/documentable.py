from typing import Optional
from typing_extensions import Protocol

from .dedentable import Dedentable


class Documentable(Dedentable, Protocol):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
