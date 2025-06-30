import abc
import typing

from fntypes.library.monad.result import Wrapped

type ValidatorResult = Wrapped[typing.Any] | typing.Any | None


class ABCValidator(abc.ABC):
    __slots__ = ()

    key: str | None = None

    def check(self, value: typing.Any, *args: str) -> ValidatorResult:
        pass


__all__ = ("ABCValidator", "ValidatorResult")
