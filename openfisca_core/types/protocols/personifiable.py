import dataclasses

from .documentable import Documentable


@dataclasses.dataclass(repr = False)
class Personifiable(Documentable):
    key: str
    plural: str
    label: str
    doc: str
