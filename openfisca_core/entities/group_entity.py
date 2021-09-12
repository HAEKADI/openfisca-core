import dataclasses
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

    .. versionchanged:: 35.7.0
        Hereafter ``variable`` allows querying a :class:`.TaxBenefitSystem`
        for a :class:`.Variable`.

    .. versionchanged:: 35.7.0
        Hereafter a :obj:`.GroupEntity` is represented by its ``key`` as
        ``GroupEntity(key)``.

    .. versionchanged:: 35.7.0
        Hereafter the equality of an :obj:`.GroupEntity` is determined by its
        data attributes.

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
    def set_tax_benefit_system(
            self,
            tax_benefit_system: Representable,
            ) -> None:
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
    def get_variable(
            self,
            variable_name: str,
            check_existence: bool = False,
            ) -> Optional[Modelable]:
        """Gets ``variable_name`` from ``variable``.

        Args:
            variable_name: The variable to be found.
            check_existence: Was the variable found? Defaults to False.

        Returns:
            :obj:`.Variable`: When the variable exists.
            None: When ``variable`` is not defined.
            None: When the variable does't exist.

        .. seealso::
            Method :meth:`.TaxBenefitSystem.get_variable`.

        .. deprecated:: 35.7.0
            :meth:`.get_variable` has been deprecated and will be
            removed in the future. The functionality is now provided by
            ``variable``.

        """

        if self.variable is None:
            return None

        return self.variable(variable_name, check_existence)

    @commons.deprecated(since = "35.7.0", expires = "the future")
    def check_variable_defined_for_entity(self, variable_name: str) -> None:
        """Checks if ``variable_name`` is defined for ``self``.

        Args:
            variable_name: The :obj:`.Variable` to be found.

        Returns:
            None: When :class:`.Variable` does not exist.
            None: When :class:`.Variable` exists, and its entity is ``self``.

        .. seealso::
            :class:`.Variable` and :attr:`.Variable.entity`.

        .. deprecated:: 35.7.0
            :meth:`.check_variable_defined_for_entity` has been deprecated and
            will be removed in the future. The functionality is now provided by
            :func:`.entities.check_variable_defined_for_entity`.

        """

        return entities.check_variable_defined_for_entity(self, variable_name)

    @staticmethod
    @commons.deprecated(since = "35.7.0", expires = "the future")
    def check_role_validity(role: Any) -> None:
        """Checks if ``role`` is an instance of :class:`.Role`.

        Args:
            role: Any object.

        Returns:
            None.

        .. deprecated:: 35.7.0
            :meth:`.check_role_validity` has been deprecated and will be
            removed in the future. The functionality is now provided by
            :func:`.entities.check_role_validity`.

        """

        return entities.check_role_validity(role)

    @staticmethod
    def _flatten(roles: Sequence[Rolifiable]) -> Sequence[Rolifiable]:
        return [array for role in roles for array in role.subroles or [role]]
