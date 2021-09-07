import pytest

from openfisca_core.entities import Entity, Role
from openfisca_core.taxbenefitsystems import TaxBenefitSystem


@pytest.fixture
def entity():
    return Entity("key", "label", "plural", "doc")


@pytest.fixture
def role(entity):
    return Role({"key": "key"}, entity)


def test_set_tax_benefit_system_deprecation(entity):
    """:meth:`.set_tax_benefit_system` throws a deprecation warning."""

    with pytest.warns(DeprecationWarning):
        entity.set_tax_benefit_system(TaxBenefitSystem([entity]))


def test_check_role_validity_deprecation(entity, role):
    """:meth:`.check_role_validity` throws a deprecation warning."""

    with pytest.warns(DeprecationWarning):
        entity.check_role_validity(role)
