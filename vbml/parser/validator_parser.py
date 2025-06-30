from __future__ import annotations

import dataclasses
import re
import typing
from collections.abc import Callable

from fntypes.library.monad.result import Error, Ok, Result

from vbml.misc import flatten
from vbml.parser.argument_parser import Argument

type ArgumentName = str
type Nesting = Callable[[dict[str, typing.Any]], dict[str, typing.Any] | None]
type ValidatorArguments = list[str]
type ValidatorName = str

VALIDATOR_ARGUMENT: typing.Final[str] = r"\[(.+)+\]"
VALIDATORS: typing.Final[re.Pattern[str]] = re.compile(r":([a-zA-Z0-9_, ]+|[\[]+[a-zA-Z0-9_, ]+[\]]+)", re.MULTILINE)


def parse_validation(validator: ValidatorName, argument_node: str, /) -> list[str]:
    arguments: list[str] = re.findall(f":{validator}{VALIDATOR_ARGUMENT}", argument_node)
    return flatten([argument.split(",") for argument in arguments])


def get_validators(
    arguments: list[Argument],
    nestings: dict[str, Nesting] | None = None,
) -> Result[list[Validator], str]:
    nestings = nestings or {}
    all_validators = list[Validator]()

    for argument in arguments:
        validators: list[str] = VALIDATORS.findall(argument.node)

        for validator in validators:
            validator_nestings = dict[str, Nesting]()
            validation = dict[str, list[str]]()

            if validator.startswith("[") and validator.endswith("]"):
                for nesting in validator.removeprefix("[").removesuffix("]").strip().split(sep=","):
                    if nesting not in nestings:
                        return Error(f"`{nesting}` is undefined in implemented nestings.")

                    validator_nestings[nesting] = nestings[nesting]
            else:
                validation[validator] = parse_validation(validator, argument.node)

            all_validators.append(Validator(argument.name, validation, validator_nestings))

    return Ok(all_validators)


@dataclasses.dataclass(frozen=True, slots=True)
class Validator:
    argument: ArgumentName
    validation: dict[ValidatorName, ValidatorArguments]
    nestings: dict[ValidatorName, Nesting]


__all__ = ("Validator", "get_validators")
