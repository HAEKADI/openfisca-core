import abc
import dataclasses

from ._documentable import _Documentable


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(_Documentable, abc.ABC):
    ...
