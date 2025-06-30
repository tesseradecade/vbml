from __future__ import annotations

import dataclasses
import re
import typing

from vbml.parser.syntax import SYNTAX_MAP, Syntax

if typing.TYPE_CHECKING:
    from vbml.parser.validator_parser import ArgumentName, Nesting, ValidatorArguments, ValidatorName
    from vbml.pattern.pattern import Pattern

type Inclusion = str


@dataclasses.dataclass(slots=True)
class RecursionArgument:
    value: str
    create_pattern_data: dict[str, typing.Any]


@dataclasses.dataclass(slots=True)
class Validator:
    name: ArgumentName
    validation: dict[ValidatorName, ValidatorArguments]
    nested: dict[ValidatorName, Nesting]


class AheadValidation:
    __slots__ = ("pattern", "inclusions", "nestings", "recursions")

    def __init__(
        self,
        pattern: type[Pattern],
        inclusions: dict[str, Inclusion | None],
        nestings: list[Nesting],
        recursions: dict[str, RecursionArgument],
    ) -> None:
        self.pattern = pattern
        self.inclusions = inclusions
        self.nestings = nestings
        self.recursions = recursions

    def get_groupdict(self, __match: re.Match[str]) -> dict[str, typing.Any] | None:
        groupdict = __match.groupdict()

        for argument, inclusion in self.inclusions.items():
            if not argument or (syntax := SYNTAX_MAP.get(argument[0])) is None:
                continue

            match syntax:
                case Syntax.UNION as union:
                    argument_name = argument.removeprefix(union)
                    groupdict[argument_name] = [argument for argument in groupdict[argument_name].split(sep=inclusion) if argument]
                case Syntax.RECURSION as recursion:
                    argument_name = argument.removeprefix(recursion)
                    pattern = self.pattern(**self.recursions[argument].create_pattern_data)

                    if not pattern.parse(groupdict[argument_name]):
                        return None

                    groupdict[argument_name] = pattern.dict()
                case _:
                    pass

        for nested in self.nestings:
            groupdict |= nested(groupdict) or {}

        return groupdict


__all__ = ("AheadValidation", "RecursionArgument", "Validator")
