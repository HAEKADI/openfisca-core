import dataclasses
import os
import textwrap
from typing import Any, ClassVar, Iterable, Optional, Sequence

from openfisca_core import commons
from openfisca_core.commons import MethodDescriptor
from openfisca_core.types import (
    Buildable,
    Descriptable,
    Modelable,
    Representable,
    Rolifiable,
    RoleLike,
    )

from .. import entities
from .role import Role
from .role_builder import RoleBuilder


@dataclasses.dataclass(repr = False)
class GroupEntity:
    """Represents a :class:`.GroupEntity` on which calculations can be run.

    A :class:`.GroupEntity` is basically a group of people, and thus it is
    composed of several :obj:`Entity` with different :obj:`Role` within the
    group. For example a tax household, a family, a trust, etc.

    Attributes:
        key (:obj:`str`): Key to identify the :class:`.GroupEntity`.
        plural (:obj:`str`): The ``key``, pluralised.
        label (:obj:`str`): A summary description.
        doc (:obj:`str`): A full description, dedented.
        roles (List[Role]): A list of the roles of the group entity.
        roles_description(List[dict]): A list of the role attributes.
        flattened_roles(List[Role]): ``roles`` flattened out.
        is_person (:obj:`bool`): Represents an individual? Defaults to False.
        variable (:obj:`callable`, optional): Find a :class:`.Variable`.

    Args:
        key: Key to identify the :class:`.GroupEntity`.
        plural: ``key``, pluralised.
        label: A summary description.
        doc: A full description.
        roles: The list of :class:`.Role` of the :class:`.GroupEntity`.

    Examples:
        >>> roles = [{
        ...     "key": "parent",
        ...     "subroles": ["first_parent", "second_parent"],
        ...     }]
        >>> GroupEntity(
        ...     "household",
        ...     "households",
        ...     "A household",
        ...     "All the people who live together in the same place.",
        ...     roles
        ...    )
        GroupEntity(household)

    """

    key: str
    plural: str
    label: str
    doc: str
    roles: dataclasses.InitVar[Iterable[RoleLike]]

    #: bool: A group entity represents several individuals.
    #:
    #: .. versionchanged:: 35.7.0
    #:    Hereafter declared as a class variable instead of as an attribute.
    #:
    is_person: ClassVar[bool] = False

    #: :class:`.Descriptable`: Find a :class:`.Variable`.
    #:
    #: .. versionadded:: 35.7.0
    #:
    variable: Descriptable[Modelable] = dataclasses.field(
        init = False,
        compare = False,
        default = MethodDescriptor("variable"),
        )

    def __post_init__(self, roles: Iterable[RoleLike]) -> None:
        self.doc = textwrap.dedent(self.doc)

        # Useless step kept to avoid changing the signature.
        self.roles_description: Iterable[RoleLike]
        self.roles_description = roles

        # Create builder.
        builder: Buildable[GroupEntity, Rolifiable, RoleLike]
        builder = RoleBuilder(self, Role)

        # Build roles & assign role attributes.
        self.roles: Sequence[Rolifiable]
        self.roles = builder(roles)
        for role in self.roles:
            self.__dict__.update({role.key.upper(): role})

        # Assign sub-role attributes.
        self.flattened_roles: Sequence[Rolifiable]
        self.flattened_roles = self._flatten(self.roles)
        for role in self.flattened_roles:
            self.__dict__.update({role.key.upper(): role})

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.key})"

    @commons.deprecated(since = "35.7.0", expires = "the future")
    def set_tax_benefit_system(self, tax_benefit_system: Representable) -> None:
        """Sets ``variable``.

        Args:
            tax_benefit_system: To query variables from.

        .. deprecated:: 35.7.0
            :meth:`.set_tax_benefit_system` has been deprecated and will be
            removed in the future. The functionality is now provided by
            ``variable``.

        """

        self.variable = tax_benefit_system.get_variable

    @commons.deprecated(since = "35.7.0", expires = "the future")
    def get_variable(self, variable_name: str, check_existence: bool = False) -> Optional[Modelable]:
        """Gets ``variable_name`` from ``variable``.

        Args:
            variable_name: The variable to be found.
            check_existence: Was the variable found? Defaults to False.

        Returns:
            :obj:`.Variable`: When the variable exists.
            None: When ``variable`` is not defined.
            None: When the variable does't exist.

        Raises:
            :exc:`.VariableNotFoundError`: When the variable doesn't exist and
                ``check_existence`` is True.

        .. seealso::
            Method :meth:`.TaxBenefitSystem.get_variable`.

        .. versionchanged:: 35.7.0
            Now also returns None when ``variable`` is not defined.

        .. deprecated:: 35.7.0
            :meth:`.get_variable` has been deprecated and will be
            removed in the future. The functionality is now provided by
            ``variable``.

        """

        if self.variable is None:
            return None

        return self.variable(variable_name, check_existence)

    def check_variable_defined_for_entity(self, variable_name: str) -> None:
        """Checks if ``variable_name`` is defined for :obj:`.Entity`.

        Note:
            This should be extracted to a helper function.

        Args:
            variable_name: The :class:`.Variable` to be found.

        Returns:
            None: When :class:`.Variable` does not exist.
            None: When :class:`.Variable` exists, and its entity is ``self``.

        Raises:
            ValueError: When the :obj:`.Variable` exists but its :obj:`.Entity`
                is not ``self``.

        Examples:
            >>> from openfisca_core.taxbenefitsystems import TaxBenefitSystem
            >>> from openfisca_core.variables import Variable
            >>> from .entity import Entity

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
            >>> group_entity
            GroupEntity(household)

            >>> class ThatVariable(Variable):
            ...     definition_period = "month"
            ...     value_type = float
            ...     entity = group_entity

            >>> tbs = TaxBenefitSystem([entity, group_entity])
            >>> tbs.load_variable(ThatVariable)
            <openfisca_core.entities.group_entity.ThatVariable...

            >>> group_entity.variable = tbs.get_variable
            >>> group_entity.check_variable_defined_for_entity("ThatVariable")

        .. seealso::
            :class:`.Variable` and :attr:`.Variable.entity`.

        .. versionchanged:: 35.7.0
            Hereafter returns None when :class:`.Variable` is not found.

        .. versionchanged:: 35.7.0
            Hereafter returns None when ``variable`` is not defined.

        .. versionchanged:: 35.7.0
            Hereafter checks for equality instead of just ``key``.

        """

        if self.variable is None:
            return None

        variable = self.variable(variable_name, check_existence = True)

        if variable is not None:
            entity = variable.entity

            if entity != self:
                message = os.linesep.join([
                    f"You tried to compute the variable '{variable_name}' for",
                    f"the entity '{self.plural}'; however the variable",
                    f"'{variable_name}' is defined for '{entity.plural}'.",
                    "Learn more about entities in our documentation:",
                    "<https://openfisca.org/doc/coding-the-legislation/50_entities.html>.",
                    ])
                raise ValueError(message)

        return None

    @staticmethod
    @commons.deprecated(since = "35.7.0", expires = "the future")
    def check_role_validity(role: Any) -> None:
        """Checks if ``role`` is an instance of :class:`.Role`.

        Args:
            role: Any object.

        Returns:
            None.

        Raises:
            :exc:`ValueError`: When ``role`` is not a :class:`.Role`.

        .. deprecated:: 35.7.0
            :meth:`.check_role_validity` has been deprecated and will be
            removed in the future. The functionality is now provided by
            :func:`.entities.check_role_validity`.

        """

        return entities.check_role_validity(role)

    @staticmethod
    def _flatten(roles: Sequence[Rolifiable]) -> Sequence[Rolifiable]:
        return [array for role in roles for array in role.subroles or [role]]
