from abc import ABC, abstractmethod
import typing
from typing_extensions import Protocol


class FuncBasedValidatorCallable(Protocol):
    def __call__(self, value: str, *args: typing.Any) -> typing.Optional[typing.Any]:
        ...


class ABCValidator(ABC):
    key: typing.Optional[str] = None

    @abstractmethod
    def check(self, value: str, *args) -> typing.Optional[typing.Any]:
        pass
