from __future__ import annotations

import abc
import typing
from collections.abc import Callable

from vbml.error import VBMLError
from vbml.validator.abc import ABCValidator
from vbml.validator.func import FuncBasedValidator, FuncBasedValidatorCallable
from vbml.validator.map import ValidatorsMap

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern

type ValidatorType = ABCValidator | type[ABCValidator] | FuncBasedValidatorCallable


class ABCPatcher(abc.ABC):
    __slots__ = ("disable_validators", "validators_map")

    def __init__(
        self,
        disable_validators: bool = False,
        validators_map: ValidatorsMap | None = None,
    ) -> None:
        self.disable_validators = disable_validators
        self.validators_map = validators_map or ValidatorsMap()

    def validator[Validator: ValidatorType](self, key: str | None = None) -> Callable[[Validator], Validator]:
        def wrapper(validator: typing.Any) -> typing.Any:
            validator_handler: ValidatorType = typing.cast("ValidatorType", validator)
            if isinstance(validator_handler, type):
                validator = validator_handler()

            elif isinstance(validator_handler, Callable):
                if not key:
                    raise VBMLError("No key is defined for validator callable.")

                validator = FuncBasedValidator(key, validator_handler)

            if not isinstance(validator, ABCValidator):
                raise VBMLError("Validator must inherit from `ABCValidator`.")

            if not key and not validator.key:
                raise VBMLError("No key is defined for validator instance.")

            self.validators_map.add(validator)

        return wrapper

    @abc.abstractmethod
    def check(
        self,
        pattern: ABCPattern,
        text: str,
        ignore_validation: bool = False,
    ) -> bool | dict[str, typing.Any] | None:
        pass


__all__ = ("ABCPatcher",)
