from vbml.patcher.abc import ABCPatcher
from vbml.pattern import Pattern
from vbml.utils.exception import ParseError
import typing


class Patcher(ABCPatcher):
    """ Main patcher to parse and validate
    Patcher documentation: https://github.com/tesseradecade/vbml/blob/master/docs/patcher.md
    """

    def check(
        self, pattern: Pattern, text: str, ignore_validation: bool = False
    ) -> typing.Optional[typing.Union[typing.Dict[typing.Any, typing.Any], bool]]:
        check = pattern.parse(text)

        if ignore_validation:
            return pattern.dict() if check else False

        elif not check:
            return False

        keys = pattern.dict()

        if self.disable_validators:
            return keys

        valid_keys: typing.Optional[dict] = {}

        for key in keys:
            if valid_keys is None:
                break
            if key in pattern.validation:
                for validator in pattern.validation[key]:
                    validator_obj = self.validators_map.get(validator)

                    if validator_obj is None:
                        raise ParseError(f"Unknown validator: {validator}")

                    args = pattern.validation[key][validator] or []
                    valid = self.validators_map.get(validator).check(keys[key], *args)

                    if valid is None:
                        valid_keys = None
                        break
                    valid_keys[key] = valid

            elif valid_keys is not None:
                valid_keys[key] = keys[key]

        pattern.pregmatch = valid_keys
        return valid_keys
