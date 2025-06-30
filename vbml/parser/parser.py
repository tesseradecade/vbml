from __future__ import annotations

import dataclasses
import typing
from collections import deque

from fntypes.library.monad.option import Nothing, Option, Some
from fntypes.library.monad.result import Error, Ok, Result
from fntypes.library.unwrapping import unwrapping

import vbml.parser.argument_parser
from vbml.parser.argument_parser import (
    parse_argument_names,
    parse_arguments,
    parse_default_validated_arguments,
    parse_validated_arguments,
)
from vbml.parser.inclusion_parser import parse_inclusion
from vbml.parser.syntax import SYNTAX_MAP, Argument, Syntax, SyntaxPattern, escape
from vbml.parser.validator_parser import Nesting, Validator, get_validators

ARGUMENT: typing.Final[str] = "<A{}>"


def escape_pattern(pattern: str, arguments: deque[vbml.parser.argument_parser.Argument], /) -> str:
    for index, argument in enumerate(arguments, start=1):
        pattern = pattern.replace(argument.node, ARGUMENT.format(index))

    return escape(pattern)


@unwrapping
def parse(
    pattern: str,
    /,
    *,
    lazy: bool = True,
    default_validators: list[str] | None = None,
    nestings: dict[str, Nesting] | None = None,
) -> Result[Pattern, str]:
    arguments = parse_arguments(pattern)
    validated_arguments = (
        parse_default_validated_arguments(arguments, default_validators) if default_validators is not None else parse_validated_arguments(arguments)
    )
    argument_names = parse_argument_names(arguments)
    validators = get_validators(validated_arguments, nestings).unwrap()
    recursion_patterns: dict[str, SyntaxPattern] = {}
    inclusions = dict(zip(argument_names, [parse_inclusion(argument) for argument in arguments]))
    pattern = escape_pattern(pattern, arguments)

    for index, argument_name in enumerate(argument_names, start=1):
        if not argument_name:
            return Error("Argument name cannot be empty.")

        syntax = SYNTAX_MAP.get(argument_name[0])
        inclusion = inclusions.get(argument_name, Nothing())
        syntax_argument = Argument(Some(argument_name), inclusion)

        match syntax:
            case Syntax():
                syntax_pattern = syntax(syntax_argument).unwrap()
                generated_pattern = syntax_pattern.pattern

                if syntax_pattern.syntax == Syntax.RECURSION:
                    recursion_patterns[argument_name] = syntax_pattern
            case _:
                pre = inclusion.unwrap_or("")
                generated_pattern = f"(?P<{argument_name}>{pre}.*{'?' if lazy else ''})"

        pattern = pattern.replace(ARGUMENT.format(index), generated_pattern)

    return Ok(
        Pattern(
            pattern=pattern,
            arguments=arguments,
            argument_names=argument_names,
            validators=tuple(validators),
            inclusions=inclusions,
            recursion_patterns=recursion_patterns,
        ),
    )


@dataclasses.dataclass(slots=True, frozen=True)
class Pattern:
    pattern: str
    arguments: deque[vbml.parser.argument_parser.Argument]
    argument_names: list[str]
    validators: tuple[Validator, ...]
    inclusions: dict[str, Option[str]]
    recursion_patterns: dict[str, SyntaxPattern]

    @property
    def validators_map(self) -> dict[str, Validator]:
        return {validator.argument: validator for validator in self.validators}


__all__ = ("Pattern", "parse")
