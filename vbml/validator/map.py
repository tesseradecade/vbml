import typing
from vbml.validator.abc import ABCValidator
from vbml.utils.exception import VBMLError
from .default import default_validators


class ValidatorsMap:
    """ Storage validators
    Read the docs here: https://github.com/tesseradecade/vbml/blob/master/docs/validators-map.md
    """

    def __init__(self, add_defaults: bool = True):
        """ Init ValidatorsMap
        :param add_defaults: should validators such as int, float be added to map
        """
        self.validators_map: typing.Dict[str, ABCValidator] = {}

        if add_defaults:
            for validator in default_validators:
                self.add(validator)

    def add(self, validator: ABCValidator) -> typing.NoReturn:
        """ Add validator to map """
        if not validator.key:
            raise VBMLError("Validator key is undefined")
        self.validators_map[validator.key] = validator

    def get(self, key: str, no_error: bool = True):
        """ Get validator from map """
        validator = self.validators_map.get(key)
        if validator is None and not no_error:
            raise VBMLError(f"Validator {key!r} is undefined")
        return validator

    def pop(self, key: str) -> ABCValidator:
        """ Remove and return validator from map """
        return self.validators_map.pop(key)
