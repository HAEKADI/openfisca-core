from __future__ import annotations

import textwrap
from typing import Type, Union

from openfisca_core.types import Personifiable


class Doc:
    public_name: str = "doc"
    private_name: str = "_doc"

    def __get__(
            self,
            instance: Personifiable,
            owner: Type[Personifiable] = None,
            ) -> Union[Doc, str]:

        return getattr(instance, self.private_name, None)

    def __set__(
            self,
            instance: Personifiable,
            value: str,
            ) -> None:

        setattr(instance, self.private_name, textwrap.dedent(value))
