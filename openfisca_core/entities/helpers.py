from typing import Any, List, Optional

from openfisca_core.commons import Personifiable, Rolifiable

from . import Entity, GroupEntity


def build_entity(
        key: str,
        plural: str,
        label: str,
        doc: str = "",
        roles: Optional[List[Rolifiable]] = None,
        is_person: bool = False,
        class_override: Optional[Any] = None,
        ) -> Personifiable:
    """Builds an :class:`.Entity` or a :class:`.GroupEntity`.

    Args:
        key: Key to identify the :class:`.Entity` or :class:`.GroupEntity`.
        plural: ``key``, pluralised.
        label: A summary description.
        doc: A full description.
        roles: A list of :class:`.Role`, if it's a :class:`.GroupEntity`.
        is_person: If is an individual, or not.
        class_override: ?

    Returns:
        :class:`.Entity`: When ``is_person`` is True.
        :class:`.GroupEntity`: When ``is_person`` is False.

    Examples:
        >>> build_entity(
        ...     "syndicate",
        ...     "syndicates",
        ...     "Banks loaning jointly.",
        ...     roles = [],
        ...     )
        <openfisca_core.entities.group_entity.GroupEntity...

        >>> build_entity(
        ...     "company",
        ...     "companies",
        ...     "A small or medium company.",
        ...     is_person = True,
        ...     )
        <openfisca_core.entities.entity.Entity...

    """

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

    .. versionadded:: 35.5.0

    """

    if role is not None and not isinstance(role, Rolifiable):
        raise ValueError(f"{role} is not a valid role")
