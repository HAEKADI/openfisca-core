import os
import textwrap
from typing import Any, Optional

from openfisca_core import commons
from openfisca_core.types import Representable, Personifiable
from openfisca_core.variables import Variable

from .. import entities


class Entity(Personifiable):
    """Represents an entity on which calculations can be run.

    For example an individual, a company, etc.

    Attributes:
        key (:obj:`str`): Key to identify the :class:`.Entity`.
        plural (:obj:`str`): The :attr:`key`, pluralised.
        label (:obj:`str`): A summary description.
        doc (:obj:`str`): A full description, dedented.
        is_person (:obj:`bool`): If is an individual, or not. Defaults to True.

    Args:
        key: Key to identify the :class:`.Entity`.
        plural: ``key``, pluralised.
        label: A summary description.
        doc: A full description.

    Examples:
        >>> Entity(
        ...     "individual",
        ...     "individuals",
        ...     "An individual",
        ...     "The minimal legal entity on which a rule might be applied.",
        ...    )
        <openfisca_core.entities.entity.Entity...

    """

    is_person: bool = True
    _tax_benefit_system: Optional[Representable] = None

    @property
    def doc(self) -> str:
        return self.__doc

    @doc.setter
    def doc(self, value: str) -> None:
        self.__doc = textwrap.dedent(value)

    def set_tax_benefit_system(self, tax_benefit_system: Representable) -> None:
        """Sets :attr:`._tax_benefit_system`."""
        self._tax_benefit_system = tax_benefit_system

    @commons.deprecated(since = "35.5.0", expires = "the future")
    def check_role_validity(self, role: Any) -> None:
        """Checks if ``role`` is an instance of :class:`.Role`.

        .. deprecated:: 35.5.0
            :meth:`.check_role_validity` has been deprecated and will be
            removed in the future. The functionality is now provided by
            :func:`.entities.check_role_validity`.

        """

        return entities.check_role_validity(role)

    def get_variable(self, variable_name: str, check_existence: bool = False) -> Optional[Variable]:
        """Gets ``variable_name`` from :attr:`_tax_benefit_system`.

        Note:
            This should be called directly from :class:`.TaxBenefitSystem` or
            extracted to a helper function!

        Args:

            variable_name: The variable to be found.
            check_existence: Was the variable found? Defaults to False.

        Returns:
            :obj:`.Variable`: When the variable exists.
            None: When :attr:`_tax_benefit_system` is not defined.
            None: When the variable does't exist.

        Raises:
            :exc:`VariableNotFoundError`: When the variable doesn't exist and
            ``check_existence`` is True.

        .. seealso::
            Method :meth:``TaxBenefitSystem.get_variable`.

        .. versionchanged:: 35.5.0
            Now also returns None when :attr:`_tax_benefit_system` is not defined.

        """

        if self._tax_benefit_system is None:
            return None

        return self._tax_benefit_system.get_variable(variable_name, check_existence)

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
            :exc:`ValueError`:
                When the :obj:`.Variable` exists but its :obj:`.Entity` is not
                ``self``.

        .. seealso::
            :class:`.Variable` and :attr:`.Variable.entity`.

        .. versionchanged:: 35.5.0
            Now also returns None when :class:`.Variable` is not found.

        """

        variable = self.get_variable(variable_name, check_existence = True)

        if variable is not None:
            variable_entity = variable.entity

            # Should be this:
            # if variable_entity is not self:
            if variable_entity.key != self.key:
                message = os.linesep.join([
                    "You tried to compute the variable '{0}' for the entity '{1}';".format(variable_name, self.plural),
                    "however the variable '{0}' is defined for '{1}'.".format(variable_name, variable_entity.plural),
                    "Learn more about entities in our documentation:",
                    "<https://openfisca.org/doc/coding-the-legislation/50_entities.html>."])
                raise ValueError(message)
