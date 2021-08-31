from typing import Any

from openfisca_core.commons import Rolifiable

from . import Entity, GroupEntity


def build_entity(key, plural, label, doc = "", roles = None, is_person = False, class_override = None):
    if is_person:
        return Entity(key, plural, label, doc)
    else:
        return GroupEntity(key, plural, label, doc, roles)


def check_role_validity(role: Any) -> None:
    """Checks if ``role`` is an instance of :class:`.Role`.

    Args:
        role: Any object.

    Returns:
        None.

    Raises:
        :exc:`ValueError`: When ``role`` is not a :class:`Role`.

    Examples:
        >>> from . import Role
        >>> role = Role({"key": "key"}, object())
        >>> check_role_validity(role)

    """

    if role is not None and not isinstance(role, Rolifiable):
        raise ValueError(f"{role} is not a valid role")
