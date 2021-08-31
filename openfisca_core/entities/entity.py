import os
import textwrap

from .role import Role


class Entity:
    """Represents an entity on which calculations can be run.

    For example an individual, a company, etc.

    Attributes:
        key (:obj:`str`): Key to identify the :class:`.Entity`.
        plural (:obj:`str`): The :attr:`key`, pluralised.
        label (:obj:`str`): Summary description.
        doc (:obj:`str`): Full description.
        is_person (:obj:`bool`): If is an individual, or not. Defaults to True.
        _tax_benefit_system (:obj:`.TaxBenefitSystem`, optional): Ruleset.

    Args:
        key: :attr:`key`.
        plural: :attr:`plural`.
        label: :attr:`label`.
        doc: :attr:`doc`.

    Examples:
        >>> Entity(
        ...     "individual",
        ...     "individuals",
        ...     "An individual",
        ...     "The minimal legal entity on which a rule might be applied.",
        ...    )
        <openfisca_core.entities.entity.Entity...

    """

    def __init__(self, key: str, plural: str, label: str, doc: str) -> None:
        self.key = key
        self.label = label
        self.plural = plural
        self.doc = textwrap.dedent(doc)
        self.is_person = True
        self._tax_benefit_system = None

    def set_tax_benefit_system(self, tax_benefit_system):
        self._tax_benefit_system = tax_benefit_system

    def check_role_validity(self, role):
        if role is not None and not type(role) == Role:
            raise ValueError("{} is not a valid role".format(role))

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
