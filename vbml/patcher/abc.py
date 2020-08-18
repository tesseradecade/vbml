from abc import ABC, abstractmethod
from vbml.validator.map import ValidatorsMap
from vbml.validator.abc import ABCValidator, FuncBasedValidatorCallable
from vbml.validator.validator import FuncBasedValidator
from vbml.utils.exception import VBMLError
import typing
import types

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern


ValidatorType = typing.Union[
    FuncBasedValidatorCallable,
    typing.Type[ABCValidator],
]


class ABCPatcher(ABC):
    def __init__(
        self, disable_validators: bool = False, validators_map: ValidatorsMap = ValidatorsMap(),
    ):
        self.disable_validators = disable_validators
        self.validators_map = validators_map

    def validator(
        self, key: typing.Optional[str] = None, *args, **kwargs
    ) -> typing.Callable[[ValidatorType], ABCValidator]:
        def decorator(validator_handler: ValidatorType) -> ABCValidator:

            if isinstance(validator_handler, types.FunctionType):
                validator = FuncBasedValidator(
                    key or validator_handler.__name__, validator_handler
                )
            elif isinstance(validator_handler, types.SimpleNamespace[ABCValidator]):
                if key is not None:
                    validator_handler.key = key
                validator = validator_handler(*args, **kwargs)
            else:
                raise VBMLError(
                    f"No assignments are available for validator type {validator_handler!r}"
                )

            self.validators_map.add(validator)
            return validator

        return decorator

    @abstractmethod
    def check(
        self, pattern: "ABCPattern", text: str, ignore_validation: bool = False
    ) -> typing.Union[bool, dict]:
        pass
