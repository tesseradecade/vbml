from abc import ABC, abstractmethod
import typing


class ABCValidator(ABC):
    key: typing.Optional[str] = None

    @abstractmethod
    def check(self, value: str, *args) -> typing.Optional[typing.Any]:
        pass
