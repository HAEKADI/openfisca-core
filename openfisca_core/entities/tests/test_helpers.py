import pytest

from openfisca_core import entities


def test_check_role_validity_when_not_role():
    """Raises a ValueError when it gets an invalid role."""

    with pytest.raises(ValueError):
        entities.check_role_validity(object())
