import abc


class Representable(abc.ABC):

    @abc.abstractmethod
    def get_variable(self, variable_name, check_existence):
        ...
