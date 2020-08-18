from abc import ABC, abstractmethod
from vbml.validator.map import ValidatorsMap
from vbml.validator.abc import ABCValidator, FuncBasedValidatorCallable
from vbml.validator.validator import FuncBasedValidator
from vbml.utils.exception import VBMLError
import typing
import types

if typing.TYPE_CHECKING:
    from vbml.pattern import Pattern


ValidatorType = typing.Union[
    FuncBasedValidatorCallable, typing.Type[ABCValidator],
]


class ABCPatcher(ABC):
    """ Vbml Patcher (pattern validation)
     Read the docs here: https://github.com/tesseradecade/vbml/blob/master/docs/patcher.md
     """

    def __init__(
        self, disable_validators: bool = False, validators_map: ValidatorsMap = ValidatorsMap(),
    ):
        """ Init patcher
        :param disable_validators: if True validation will be disabled
        :param validators_map: read docs at validators-map.md
        """
        self.disable_validators = disable_validators
        self.validators_map = validators_map

    def validator(
        self, key: typing.Optional[str] = None
    ) -> typing.Callable[[ValidatorType], ABCValidator]:
        """ Used as decorator for validator. Decorated func will be wrapped with FuncBaseValidator.
        :param key: validator name
        :return: decorator
        """

        def decorator(validator_handler: ValidatorType) -> ABCValidator:
            validator: ABCValidator

            if isinstance(validator_handler, types.FunctionType):
                validator = FuncBasedValidator(
                    key or validator_handler.__name__, validator_handler
                )
            elif issubclass(validator_handler, ABCValidator):  # type: ignore
                if key is not None:
                    validator_handler.key = key
                validator = validator_handler()  # type: ignore
            else:
                raise VBMLError("Validator's type is undefined")

            self.validators_map.add(validator)
            return validator

        return decorator

    @abstractmethod
    def check(
        self, pattern: "Pattern", text: str, ignore_validation: bool = False
    ) -> typing.Optional[typing.Union[typing.Dict[typing.Any, typing.Any], bool]]:
        """ Parse and validate pattern
        :param pattern: validated pattern
        :param text: validated text
        :param ignore_validation: just parse pattern
        :return: None if validation failed, False if parsing failed, dict if validation succeed
        """
        pass
