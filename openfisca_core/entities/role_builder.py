from __future__ import annotations

from typing import List, Type

from openfisca_core.types import Personifiable, Rolifiable, RoleLike, Roles


class RoleBuilder:

    def __init__(self, cls: Type[Rolifiable], entity: Personifiable) -> None:
        self.cls = cls
        self.entity = entity

    def __call__(self, roles: Roles) -> List[Rolifiable]:
        return [self.build(desc) for desc in roles]

    def build(self, desc: RoleLike) -> Rolifiable:
        role = self.cls(desc, self.entity)
        self.entity.__dict__[role.key.upper()] = role
        subroles = desc.get("subroles", [])

        if subroles:
            role.subroles = [self.build({"key": key, "max": 1}) for key in subroles]
            role.max = len(role.subroles)

        return role
