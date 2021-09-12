import dataclasses
import textwrap
from typing import Any, ClassVar, Optional

from openfisca_core import commons
from openfisca_core.commons import MethodDescriptor
from openfisca_core.types import Descriptable, Modelable, Representable

from .. import entities


@dataclasses.dataclass(repr = False)
class Entity:
    """Represents an entity on which calculations can be run.

    For example an individual, a company, etc.

    Attributes:
        key (:obj:`str`): Key to identify the :class:`.Entity`.
        plural (:obj:`str`): The ``key``, pluralised.
        label (:obj:`str`): A summary description.
        doc (:obj:`str`): A full description, dedented.
        is_person (:obj:`bool`): Represents an individual? Defaults to True.
        variable (:obj:`callable`, optional): Find a :class:`.Variable`.

    Args:
        key: Key to identify the :class:`.Entity`.
        plural: ``key``, pluralised.
        label: A summary description.
        doc: A full description.

    Examples:
        >>> from openfisca_core.taxbenefitsystems import TaxBenefitSystem
        >>> from openfisca_core.variables import Variable

        >>> entity = Entity(
        ...     "individual",
        ...     "individuals",
        ...     "An individual",
        ...     "The minimal legal entity on which a rule might be applied.",
        ...    )
        >>> entity
        Entity(individual)

        >>> class Variable(Variable):
        ...     definition_period = "month"
        ...     value_type = float
        ...     entity = entity

        >>> tbs = TaxBenefitSystem([entity])
        >>> tbs.load_variable(Variable)
        <openfisca_core.entities.entity.Variable...

        >>> get_variable = tbs.get_variable
        >>> get_variable("Variable")
        <openfisca_core.entities.entity.Variable...

        >>> entity.variable = tbs.get_variable
        >>> entity.variable("Variable")
        <openfisca_core.entities.entity.Variable...

        .. versionchanged:: 35.7.0
            Hereafter ``variable`` allows querying a :class:`.TaxBenefitSystem`
            for a :class:`.Variable`.

        .. versionchanged:: 35.7.0
            Hereafter an :obj:`.Entity` is represented by its ``key`` as
            ``Entity(key)``.

        .. versionchanged:: 35.7.0
            Hereafter the equality of an :obj:`.Entity` is determined by its
            data attributes.

    """

    key: str
    plural: str
    label: str
    doc: str

    #: bool: An entity represents an individual.
    #:
    #: .. versionchanged:: 35.7.0
    #:    Hereafter declared as a class variable instead of as an attribute.
    #:
    is_person: ClassVar[bool] = True

    #: :class:`.Descriptable`: Find a :class:`.Variable`.
    #:
    #: .. versionadded:: 35.7.0
    #:
    variable: Descriptable[Modelable] = dataclasses.field(
        init = False,
        compare = False,
        default = MethodDescriptor("variable"),
        )

    def __post_init__(self) -> None:
        self.doc = textwrap.dedent(self.doc)

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
