import dataclasses
from typing import Optional

from ..data_types import SubrolesLike
from .documentable import Documentable
from .personifiable import Personifiable


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(Documentable):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    entity: Personifiable
    subroles: Optional[SubrolesLike]
