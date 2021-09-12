import os
from typing import Any, Iterable, Optional

from openfisca_core.types import Personifiable, Rolifiable, RoleLike

from .entity import Entity
from .group_entity import GroupEntity


def build_entity(
        key: str,
        plural: str,
        label: str,
        doc: str = "",
        roles: Optional[Iterable[RoleLike]] = None,
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
        :obj:`.Entity` or :obj:`.GroupEntity`:
        :obj:`.Entity`: When ``is_person`` is True.
        :obj:`.GroupEntity`: When ``is_person`` is False.

    Raises:
        ValueError: If ``roles`` is not iterable.

    Examples:
        >>> build_entity(
        ...     "syndicate",
        ...     "syndicates",
        ...     "Banks loaning jointly.",
        ...     roles = [],
        ...     )
        GroupEntity(syndicate)

        >>> build_entity(
        ...     "company",
        ...     "companies",
        ...     "A small or medium company.",
        ...     is_person = True,
        ...     )
        Entity(company)

    .. versionchanged:: 35.7.0
        Instead of raising :exc:`TypeError` when ``roles`` is None, it does
        now raise :exc:`ValueError` when ``roles`` is not iterable.

    """

    if is_person:
        return Entity(key, plural, label, doc)

    if roles is not None and hasattr(roles, "__iter__"):
        return GroupEntity(key, plural, label, doc, roles)

    raise ValueError(f"Invalid value '{roles}' for 'roles', must be iterable.")


def check_role_validity(role: Any) -> None:
    """Checks if ``role`` is an instance of :class:`.Role`.

    Args:
        role: Any object.

    Raises:
        ValueError: When ``role`` is not a :class:`.Role`.

    Examples:
        >>> from openfisca_core.entities import Role
        >>> role = Role({"key": "key"}, object())
        >>> check_role_validity(role)

    .. versionchanged:: 35.7.0
        Now also returns None when ``variable`` is not defined.

    .. versionadded:: 35.7.0

    """

    if role is not None and not isinstance(role, Rolifiable):
        raise ValueError(f"{role} is not a valid role")


def check_variable_defined_for_entity(
        entity: Personifiable,
        variable_name: str,
        ) -> None:
    """Checks if ``variable_name`` is defined for ``entity``.

    Args:
        entity: An :obj:`.Entity`, a :obj:`.GroupEntity`…
        variable_name: The :obj:`.Variable` to be found.

    Returns:
        :obj:`None`:
        :obj:`None` when :class:`.Variable` does not exist.
        :obj:`None` when :class:`.Variable` exists and
        :attr:`.Variable.entity` is ``entity``.

    Raises:
        ValueError: When the :obj:`.Variable` exists but its ``entity`` is not
            ``entity``.

    Examples:
        >>> from openfisca_core.taxbenefitsystems import TaxBenefitSystem
        >>> from openfisca_core.variables import Variable

        >>> entity = Entity(
        ...     "individual",
        ...     "individuals",
        ...     "An individual",
        ...     "The minimal legal entity on which a rule can be applied.",
        ...    )

        >>> class ThisVariable(Variable):
        ...     definition_period = "month"
        ...     value_type = float
        ...     entity = entity

        >>> group_entity = GroupEntity(
        ...    "household",
        ...    "households",
        ...    "A household",
        ...    "All the people who live together in the same place.",
        ...    [],
        ...    )

        >>> class ThatVariable(Variable):
        ...     definition_period = "month"
        ...     value_type = float
        ...     entity = group_entity

        >>> tbs = TaxBenefitSystem([entity, group_entity])

        >>> tbs.load_variable(ThisVariable)
        <openfisca_core.entities.helpers.ThisVariable...

        >>> tbs.load_variable(ThatVariable)
        <openfisca_core.entities.helpers.ThatVariable...

        >>> entity.variable = tbs.get_variable
        >>> check_variable_defined_for_entity(entity, "ThisVariable")

        >>> group_entity.variable = tbs.get_variable
        >>> check_variable_defined_for_entity(group_entity, "ThatVariable")

    .. seealso::
        :class:`.Variable` and :attr:`.Variable.entity`.

    .. versionchanged:: 35.7.0
        Hereafter checks for equality instead of just ``key``.

    .. versionchanged:: 35.7.0
        Hereafter returns None when ``variable`` is not defined.

    .. versionchanged:: 35.7.0
        Hereafter returns None when :class:`.Variable` is not found.

    .. versionadded:: 35.7.0

    """

    if entity.variable is None:
        return None

    variable = entity.variable(variable_name, check_existence = True)

    if variable is not None:
        other = variable.entity

        if entity != other:
            message = os.linesep.join([
                f"You tried to compute the variable '{variable_name}' for",
                f"the entity '{entity.plural}'; however the variable",
                f"'{variable_name}' is defined for '{other.plural}'.",
                "Learn more about entities in our documentation:",
                "<https://openfisca.org/doc/coding-the-legislation/50_entities.html>.",
                ])
            raise ValueError(message)

    return None
