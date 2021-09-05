import abc
import dataclasses
from typing import Optional

from . import Documentable


@dataclasses.dataclass(repr = False)
class Personifiable(Documentable, abc.ABC):

    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: str
