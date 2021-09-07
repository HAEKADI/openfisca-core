from __future__ import annotations

from typing import Optional, Sequence

import typing_extensions
from typing_extensions import Protocol

from .documentable import Documentable
from .personifiable import Personifiable


@typing_extensions.runtime_checkable
class Rolifiable(Documentable, Protocol):
    entity: Personifiable
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    subroles: Optional[Sequence[Rolifiable]]
