from abc import ABC, abstractmethod
import typing
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class FuncBasedValidatorCallable(Protocol):
    """ Used to derive func to FuncBasedValidator with typings """

    key: typing.Optional[str] = None

    def __call__(self, value: str, *args: typing.Any) -> typing.Optional[typing.Any]:
        ...


class ABCValidator(ABC):
    """ Parent of all validators. Key field is required """

    key: typing.Optional[str] = None

    @abstractmethod
    def check(self, value: str, *args) -> typing.Optional[typing.Any]:
        pass
