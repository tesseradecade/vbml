from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern


class ABCPatcher(ABC):
    @abstractmethod
    def __init__(
        self,
        disable_validators: bool = False,
        validators_map: typing.Optional[bool] = None,
    ):
        self.disable_validators = disable_validators
        self.validators_map = validators_map

    @abstractmethod
    def check(self, text: str, pattern: "ABCPattern", ignore_validation: bool = False):
        pass
