import dataclasses
from typing import Optional

from ..data_types import SubrolesLike, RoleLike
from .documentable import Documentable
from .personifiable import Personifiable


@dataclasses.dataclass(repr = False)
class Rolifiable(Documentable):
    key: str
    plural: Optional[str] = None
    label: Optional[str] = None
    doc: Optional[str] = None
    max: Optional[int] = None
    subroles: Optional[SubrolesLike] = None

    def __init__(self, description: RoleLike, entity: Personifiable) -> None:
        ...
