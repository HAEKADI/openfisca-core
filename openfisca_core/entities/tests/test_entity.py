import pytest

from openfisca_core.entities import Entity, Role


def test_check_role_validity_deprecation():
    """check_role_validity() throws a deprecation warning when used."""

    entity = Entity("key", "label", "plural", "doc")
    role = Role({"key": "key"}, entity)

    with pytest.warns(DeprecationWarning):
        entity.check_role_validity(role)
