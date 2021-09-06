import abc
from typing import Any, Optional
from typing_extensions import Protocol


class Representable(Protocol):

    @abc.abstractmethod
    def get_variable(
            self,
            variable_name: str,
            check_existence: bool = False,
            ) -> Optional[Any]:
        ...
