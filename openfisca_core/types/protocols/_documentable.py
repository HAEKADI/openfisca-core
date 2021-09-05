import abc
import dataclasses
from typing import Optional
from typing_extensions import Protocol


@dataclasses.dataclass
class _Documentable(Protocol):

    key: str
    plural: Optional[str]
    label: Optional[str]

    @property
    @abc.abstractproperty
    def doc(self) -> str:
        ...

    @doc.setter
    def doc(self, value: str) -> None:
        ...
