from typing import List, TypeVar

from .dicts import RoleLike


Args = List
T = TypeVar("T", bound = Args)

Roles = List[RoleLike]
