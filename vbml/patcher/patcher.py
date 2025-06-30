from __future__ import annotations

import typing

from fntypes.library.misc import is_err, is_ok
from fntypes.library.monad.option import Nothing

from vbml.error import ParseError
from vbml.patcher.abc import ABCPatcher
from vbml.pattern.pattern import Pattern

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern


class Patcher(ABCPatcher):
    __slots__ = ()

    def validate(self, pattern: Pattern, data: dict[str, typing.Any]) -> dict[str, typing.Any] | None:
        validated: dict[str, typing.Any] | None = {}

        for key, value in data.items():
            if validated is None:
                break

            if key in pattern.validation:
                for validator in pattern.validation[key]:
                    validator_obj = self.validators_map.get(validator)

                    if validator_obj is None:
                        raise ParseError(f"Unknown validator `{validator}`.")

                    args = pattern.validation[key][validator]
                    result = self.validators_map.get(validator, no_error=False).check(value, *args)

                    if result is None or is_err(result):
                        if result is not None and not isinstance(result, Nothing):
                            result.unwrap()

                        validated = None
                        break

                    validated[key] = result if not is_ok(result) else result.unwrap()
            else:
                validated[key] = value

        if validated is not None:
            pattern.pregmatch = validated

        return validated

    def check(
        self,
        pattern: ABCPattern,
        text: str,
        ignore_validation: bool = False,
    ) -> dict[str, typing.Any] | typing.Literal[False, None]:
        parsed = pattern.parse(text)

        if ignore_validation:
            return pattern.dict() if parsed else False

        if not parsed:
            return False

        data = pattern.dict()
        if not self.disable_validators and isinstance(pattern, Pattern):
            return self.validate(pattern, data)

        return data


__all__ = ("Patcher",)
