import pytest

from openfisca_core.entities import Entity, GroupEntity
from openfisca_core.errors import VariableNotFoundError
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.variables import Variable


@pytest.fixture
def roles():
    """A role-like."""

    return [{"key": "parent", "subroles": ["first_parent", "second_parent"]}]


@pytest.fixture
def entity():
    """An entity."""

    return Entity("key", "label", "plural", "doc")


@pytest.fixture
def group_entity(roles):
    """A group entity."""

    return GroupEntity("key", "label", "plural", "doc", roles)


@pytest.fixture
def ThisVariable(entity):
    """A variable."""

    return type(
        "ThisVariable",
        (Variable,),
        {
            "definition_period": "month",
            "value_type": float,
            "entity": entity,
            },
        )


@pytest.fixture
def ThatVariable(group_entity):
    """A variable."""

    return type(
        "ThatVariable",
        (Variable,),
        {
            "definition_period": "month",
            "value_type": float,
            "entity": group_entity,
            },
        )


@pytest.fixture
def tax_benefit_system(entity, group_entity, ThatVariable):
    """A tax-benefit system."""

    tbs = TaxBenefitSystem([entity, group_entity])
    tbs.load_variable(ThatVariable)
    return tbs


@pytest.fixture
def method(tax_benefit_system):
    """A descriptable method."""

    return tax_benefit_system.get_variable


def test_init_when_doc_indented():
    """Dedents the ``doc`` attribute if it is passed at initialisation."""

    key = "\tkey"
    doc = "\tdoc"
    group_entity = GroupEntity(key, "label", "plural", doc, [])
    assert group_entity.key == key
    assert group_entity.doc != doc


def test_variable_when_not_set(group_entity):
    """Returns None when not yet defined."""

    assert not group_entity.variable


def test_variable_query_when_not_set(group_entity):
    """Raises TypeError when called and not yet defined."""

    with pytest.raises(TypeError):
        group_entity.variable("variable")


def test_set_tax_benefit_system_deprecation(group_entity, tax_benefit_system):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        group_entity.set_tax_benefit_system(tax_benefit_system)


def test_check_role_validity_deprecation(group_entity):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        group_entity.check_role_validity(group_entity.PARENT)


def test_get_variable_deprecation(group_entity):
    """Throws a deprecation warning when called."""

    with pytest.warns(DeprecationWarning):
        group_entity.get_variable("variable")


def test_check_variable_defined_for_entity_when_no_descriptor(group_entity):
    """Returns None when there is no descriptor set."""

    assert not group_entity.check_variable_defined_for_entity("asdf")


def test_check_variable_defined_for_entity_when_no_var(group_entity, method):
    """Raises VariableNotFoundError when the variable is not found."""

    group_entity.variable = method

    with pytest.raises(VariableNotFoundError):
        group_entity.check_variable_defined_for_entity("asdf")


def test_check_variable_defined_for_entity_when_diff_entity(roles, method):
    """Raises ValueError when a variable is found but for another entity."""

    group_entity = GroupEntity("another-key", "label", "plural", "doc", roles)
    group_entity.variable = method

    with pytest.raises(ValueError):
        group_entity.check_variable_defined_for_entity("ThatVariable")


def test_group_entity_with_roles(group_entity):
    """Assigns a :obj:`.Role` for each role-like passed as argument."""

    assert group_entity.PARENT


def test_group_entity_with_subroles(group_entity):
    """Assigns a :obj:`.Role` for each subrole-like passed as argument."""

    assert group_entity.FIRST_PARENT
