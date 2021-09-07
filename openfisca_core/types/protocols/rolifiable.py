from __future__ import annotations

import abc
from typing import Optional, Sequence

import typing_extensions
from typing_extensions import Protocol

from ..data_types import RoleLike
from .documentable import Documentable
from .personifiable import Personifiable


@typing_extensions.runtime_checkable
class Rolifiable(Documentable, Protocol):
    entity: Personifiable
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: str
    max: Optional[int]
    subroles: Optional[Sequence[Rolifiable]]

    @abc.abstractmethod
    def __init__(self, description: RoleLike, entity: Personifiable) -> None:
        ...
