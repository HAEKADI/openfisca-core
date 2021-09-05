import abc
import dataclasses

from . import Personifiable


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(Personifiable, abc.ABC):
    ...
