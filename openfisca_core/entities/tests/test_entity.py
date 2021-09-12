import pytest

from openfisca_core.entities import Entity, Role
from openfisca_core.errors import VariableNotFoundError
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.variables import Variable


@pytest.fixture
def entity():
    """An entity."""

    return Entity("key", "label", "plural", "doc")


@pytest.fixture
def role(entity):
    """A role."""

    return Role({"key": "key"}, entity)


@pytest.fixture
def MyVariable(entity):
    """A variable."""

    return type(
        "MyVariable",
        (Variable,),
        {
            "definition_period": "month",
            "value_type": float, "entity":
            entity,
            },
        )


@pytest.fixture
def tax_benefit_system(entity, MyVariable):
    """A tax-benefit system."""

    tbs = TaxBenefitSystem([entity])
    tbs.load_variable(MyVariable)
    return tbs


@pytest.fixture
def method(tax_benefit_system):
    """A descriptable method."""

    return tax_benefit_system.get_variable


def test_init_when_doc_indented():
    """Dedents the ``doc`` attribute if it is passed at initialisation."""

    key = "\tkey"
    doc = "\tdoc"
    entity = Entity(key, "label", "plural", doc)
    assert entity.key == key
    assert entity.doc != doc


def test_variable_when_not_set(entity):
    """Returns None when not yet defined."""

    assert not entity.variable


def test_variable_query_when_not_set(entity):
    """Raises TypeError when called and not yet defined."""

    with pytest.raises(TypeError):
        entity.variable("variable")


def test_set_tax_benefit_system_deprecation(entity, tax_benefit_system):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        entity.set_tax_benefit_system(tax_benefit_system)


def test_check_role_validity_deprecation(entity, role):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        entity.check_role_validity(role)


def test_get_variable_deprecation(entity):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        entity.get_variable("variable")


def test_check_variable_defined_for_entity_when_no_descriptor(entity):
    """Returns None when there is no descriptor set."""

    assert not entity.check_variable_defined_for_entity("asdf")


def test_check_variable_defined_for_entity_when_no_variable(entity, method):
    """Raises VariableNotFoundError when the variable is not found."""

    entity.variable = method

    with pytest.raises(VariableNotFoundError):
        entity.check_variable_defined_for_entity("asdf")


def test_check_variable_defined_for_entity_when_different_entity(method):
    """Raises ValueError when a variable is found but for another entity."""

    entity = Entity("another-key", "label", "plural", "doc")
    entity.variable = method

    with pytest.raises(ValueError):
        entity.check_variable_defined_for_entity("MyVariable")
