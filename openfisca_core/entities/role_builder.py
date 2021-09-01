from __future__ import annotations

from typing import List, Type

from .. import entities


class RoleBuilder:

    def __init__(self, cls: Type[entities.Role], entity: entities.GroupEntity) -> None:
        self.cls = cls
        self.entity = entity

    def __call__(self, roles: list) -> List[entities.Role]:
        return [self.build(desc) for desc in roles]

    def build(self, desc: dict) -> entities.Role:
        role = self.cls(desc, self.entity)
        self.entity.__dict__[role.key.upper()] = role
        subroles = desc.get("subroles", [])

        if subroles:
            role.subroles = [self.build({"key": key, "max": 1}) for key in subroles]
            role.max = len(role.subroles)

        return role
