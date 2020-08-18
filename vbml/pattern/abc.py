from abc import ABC, abstractmethod
import typing


class ABCPattern(ABC):
    @abstractmethod
    def __init__(
        self, text: typing.Optional[str] = None, regex: str = "{}$", lazy: bool = True, **context
    ):
        pass

    @abstractmethod
    def parse(self, text: str) -> typing.Optional[bool]:
        pass

    @abstractmethod
    def dict(self) -> dict:
        pass
