import os
from typing import Optional

from openfisca_core.commons import Representable, Personifiable

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

    def set_tax_benefit_system(self, tax_benefit_system: Representable) -> None:
        """Sets :attr:`._tax_benefit_system`."""
        self._tax_benefit_system = tax_benefit_system

    def get_variable(self, variable_name, check_existence = False):
        return self._tax_benefit_system.get_variable(variable_name, check_existence)

    def check_variable_defined_for_entity(self, variable_name):
        variable_entity = self.get_variable(variable_name, check_existence = True).entity
        # Should be this:
        # if variable_entity is not self:
        if variable_entity.key != self.key:
            message = os.linesep.join([
                "You tried to compute the variable '{0}' for the entity '{1}';".format(variable_name, self.plural),
                "however the variable '{0}' is defined for '{1}'.".format(variable_name, variable_entity.plural),
                "Learn more about entities in our documentation:",
                "<https://openfisca.org/doc/coding-the-legislation/50_entities.html>."])
            raise ValueError(message)
