from typing import Optional
from typing_extensions import Protocol


class Documentable(Protocol):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
