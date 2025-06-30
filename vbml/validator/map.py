import typing

from vbml.error import VBMLError
from vbml.validator.abc import ABCValidator
from vbml.validator.default import default_validators


class ValidatorsMap:
    validators_map: dict[str, ABCValidator]

    __slots__ = ("validators_map",)

    def __init__(self, add_defaults: bool = True) -> None:
        self.validators_map = {}

        if add_defaults:
            for validator in default_validators:
                self.add(validator)

    def add(self, validator: ABCValidator) -> None:
        if not validator.key:
            raise VBMLError("Validator key is empty or undefined.")

        self.validators_map[validator.key] = validator

    @typing.overload
    def get(self, key: str, no_error: typing.Literal[False]) -> ABCValidator: ...

    @typing.overload
    def get(self, key: str, no_error: bool = True) -> ABCValidator | None: ...

    @typing.no_type_check
    def get(self, key: str, no_error: bool = True) -> ABCValidator | None:
        validator = self.validators_map.get(key, None)

        if validator is None and not no_error:
            raise VBMLError(f"Validator {key!r} is undefined.")

        return validator

    def pop(self, key: str) -> ABCValidator:
        return self.validators_map.pop(key)


__all__ = ("ValidatorsMap",)
