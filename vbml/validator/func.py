import typing
from collections.abc import Callable

from vbml.validator.abc import ABCValidator, ValidatorResult

type FuncBasedValidatorCallable = Callable[typing.Concatenate[str, ...], ValidatorResult]


class FuncBasedValidator(ABCValidator):
    __slots__ = ("key", "func")

    def __init__(self, key: str, func: FuncBasedValidatorCallable) -> None:
        self.key = key
        self.func = func

    def check(self, value: typing.Any, *args: str) -> ValidatorResult:
        return self.func(value, *args)


__all__ = ("FuncBasedValidator", "FuncBasedValidatorCallable")
