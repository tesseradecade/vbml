from .abc import ABCValidator, FuncBasedValidatorCallable
import typing


class FuncBasedValidator(ABCValidator):
    def __init__(self, key: str, func: FuncBasedValidatorCallable):
        self.key = key
        self.func = func

    def check(self, value: str, *args) -> typing.Optional[typing.Any]:
        return self.func(value, *args)
