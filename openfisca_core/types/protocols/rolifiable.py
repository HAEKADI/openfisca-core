from __future__ import annotations

from typing import Optional, Sequence

from typing_extensions import Protocol

from .documentable import Documentable
from .personifiable import Personifiable


class Rolifiable(Documentable, Protocol):
    entity: Personifiable
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    subroles: Optional[Sequence[Rolifiable]]
