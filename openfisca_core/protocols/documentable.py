import abc
import textwrap


class Documentable(abc.ABC):

    @property
    def doc(self) -> str:
        return self.__doc

    @doc.setter
    def doc(self, value: str) -> None:
        self.__doc = textwrap.dedent(value)
