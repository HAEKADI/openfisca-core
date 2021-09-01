from __future__ import annotations

from typing import Optional

from openfisca_core.commons import Rolifiable

from .. import entities


class Role(Rolifiable):
    """Role of an :class:`.Entity` within a :class:`.GroupEntity`.

    Each :class:`.Entity` related to a :class:`.GroupEntity` has a
    :class:`.Role`. For example, if you have a family, its roles could include
    a parent, a child, and so on. Or if you have a tax household, its roles
    could include the taxpayer, a spouse, several dependents, and so on.

    Attributes:
        key (:obj:`str`): Key to identify the :class:`.Role`.
        plural (:obj:`str`, optional): The :attr:`key`, pluralised.
        label (:obj:`str`, optional): A summary description.
        doc (:obj:`str`, optional): A full description, dedented.
        max (:obj:`int`, optional): Max number of members. Defaults to None.
        entity (:obj:`.Entity`): :obj:`.Entity` the :class:`.Role` belongs to.
        subroles (list, optional): The ``subroles``. Defaults to None.

    Args:
        description: A dictionary containing most of the attributes.
        entity: :obj:`.Entity` the :class:`.Role` belongs to.

    Examples:
        >>> description = {
        ...     "key": "parent",
        ...     "label": "Parents",
        ...     "plural": "parents",
        ...     "doc": "The one or two adults in charge of the household.",
        ...     "max": 2,
        ...     }
        >>> Role(description, object())
        Role(parent)

    """

    max: Optional[int]
    entity: entities.Entity
    subroles: Optional[list]

    def __init__(self, description: dict, entity: entities.Entity) -> None:
        self.key = description['key']
        self.plural = description.get('plural')
        self.label = description.get('label')
        self.doc = description.get('doc', "")
        self.max = description.get('max')
        self.entity = entity
        self.subroles = None

    def __repr__(self):
        return "Role({})".format(self.key)
