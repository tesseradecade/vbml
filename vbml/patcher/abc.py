from abc import ABC, abstractmethod
from vbml.validator.map import ValidatorsMap
import typing

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern


class ABCPatcher(ABC):
    def __init__(
        self,
        disable_validators: bool = False,
        validators_map: ValidatorsMap = ValidatorsMap(),
    ):
        self.disable_validators = disable_validators
        self.validators_map = validators_map

    @abstractmethod
    def check(
        self, pattern: "ABCPattern", text: str, ignore_validation: bool = False
    ) -> typing.Union[bool, dict]:
        pass
