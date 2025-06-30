import abc
import typing


class ABCPattern(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def parse(self, text: str) -> bool:
        pass

    @abc.abstractmethod
    def dict(self) -> dict[str, typing.Any]:
        pass


__all__ = ("ABCPattern",)
