import abc
from typing_extensions import Protocol


class Representable(Protocol):

    @abc.abstractmethod
    def get_variable(self, variable_name, check_existence):
        ...
