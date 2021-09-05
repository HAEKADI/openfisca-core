import textwrap
from typing_extensions import Protocol


class Dedentable(Protocol):
    __doc: str

    @property
    def doc(self) -> str:
        return self.__doc

    @doc.setter
    def doc(self, value: str) -> None:
        self.__doc = textwrap.dedent(value)
