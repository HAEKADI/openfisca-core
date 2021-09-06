from __future__ import annotations

from typing import Iterable, Type

from openfisca_core.types import Personifiable, Rolifiable, RoleLike, RolesLike


class RoleBuilder:

    def __init__(
            self,
            builder: Personifiable,
            buildee: Type[Rolifiable],
            ) -> None:
        self.builder = builder
        self.buildee = buildee

    def __call__(self, items: RolesLike) -> Iterable[Rolifiable]:
        return [self.build(item) for item in items]

    def build(self, item: RoleLike) -> Rolifiable:
        role = self.buildee(item, self.builder)
        self.builder.__dict__[role.key.upper()] = role
        subroles = item.get("subroles", [])

        if subroles:
            role.subroles = [self.build({"key": key, "max": 1}) for key in subroles]
            role.max = len(role.subroles)

        return role
