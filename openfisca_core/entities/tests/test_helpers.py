import functools

import pytest

from openfisca_core import entities
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
def tax_benefit_system(entity, group_entity, ThisVariable, ThatVariable):
    """A tax-benefit system."""

    tbs = TaxBenefitSystem([entity, group_entity])
    tbs.load_variable(ThisVariable)
    tbs.load_variable(ThatVariable)
    return tbs


@pytest.fixture
def method(tax_benefit_system):
    """A descriptable method."""

    return tax_benefit_system.get_variable


def test_build_entity_without_roles():
    """Raises a ArgumentError when it's called without roles."""

    build_entity = functools.partial(entities.build_entity, "", "", "")

    with pytest.raises(ValueError):
        build_entity(roles = None)


def test_check_role_validity_when_not_role():
    """Raises a ValueError when it gets an invalid role."""

    with pytest.raises(ValueError):
        entities.check_role_validity(object())


def test_check_defined_for_entity_when_no_descriptor(entity, group_entity):
    """Returns None when there is no descriptor set."""

    assert not entities.check_variable_defined_for_entity(entity, "asdf")
    assert not entities.check_variable_defined_for_entity(group_entity, "asdf")


def test_check_defined_for_entity_when_no_var(entity, group_entity, method):
    """Raises VariableNotFoundError when the variable is not found."""

    entity.variable = method

    with pytest.raises(VariableNotFoundError):
        entities.check_variable_defined_for_entity(entity, "asdf")

    group_entity.variable = method

    with pytest.raises(VariableNotFoundError):
        entities.check_variable_defined_for_entity(group_entity, "asdf")


def test_check_variable_defined_for_entity_when_diff_entity(roles, method):
    """Raises ValueError when a variable is found but for another entity."""

    entity = Entity("another-key", "label", "plural", "doc")
    entity.variable = method

    with pytest.raises(ValueError):
        entities.check_variable_defined_for_entity(
            entity,
            "ThisVariable",
            )

    group_entity = GroupEntity("another-key", "label", "plural", "doc", roles)
    group_entity.variable = method

    with pytest.raises(ValueError):
        entities.check_variable_defined_for_entity(
            group_entity,
            "ThatVariable",
            )
