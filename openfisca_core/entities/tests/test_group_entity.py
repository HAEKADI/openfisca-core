import pytest

from openfisca_core.entities import GroupEntity


@pytest.fixture
def roles():
    """A role-like."""

    return [{"key": "parent", "subroles": ["first_parent", "second_parent"]}]


@pytest.fixture
def group_entity(roles):
    """A group entity."""

    return GroupEntity(
        "household",
        "households",
        "A household",
        "All the people who live together in the same place.",
        roles,
        )


def test_init_when_doc_indented():
    """Dedents the ``doc`` attribute if it is passed at initialisation."""

    key = "\tkey"
    doc = "\tdoc"
    entity = GroupEntity(key, "label", "plural", doc, [])
    assert entity.key == key
    assert entity.doc != doc


def test_group_entity_with_roles(group_entity):
    """Assigns a :obj:`.Role` for each role-like passed as argument."""

    assert str(group_entity.PARENT) == "Role(parent)"


def test_group_entity_with_subroles(group_entity):
    """Assigns a :obj:`.Role` for each subrole-like passed as argument."""

    assert group_entity.FIRST_PARENT
