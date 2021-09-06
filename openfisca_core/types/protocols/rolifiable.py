from __future__ import annotations

import dataclasses
from typing import Optional, Sequence

from ..data_types import RoleLike
from .documentable import Documentable
from .personifiable import Personifiable


@dataclasses.dataclass(repr = False)
class Rolifiable(Documentable):
    key: str
    plural: Optional[str] = None
    label: Optional[str] = None
    doc: Optional[str] = None
    max: Optional[int] = None
    subroles: Optional[Sequence[Rolifiable]] = None

    def __init__(self, description: RoleLike, entity: Personifiable) -> None:
        ...
