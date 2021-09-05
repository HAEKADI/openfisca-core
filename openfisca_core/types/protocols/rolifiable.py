import dataclasses
from typing import Optional

from .documentable import Documentable, Personifiable, SubrolesLike


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(Documentable):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    entity: Personifiable
    subroles: Optional[SubrolesLike]
