from __future__ import annotations

import dataclasses
import re
import typing
from collections import deque
from collections.abc import Iterable

from vbml.parser.syntax import Syntax

ARG_NAME: typing.Final[re.Pattern[str]] = re.compile(r"<\(.*\)([A-Za-z0-9_" + "".join(Syntax) + r"]*)\s*>", re.MULTILINE)
VALIDATED_ARGS: typing.Final[re.Pattern[str]] = re.compile(r"<\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*[^>]+?>", re.MULTILINE)


def parse_arguments(
    text: str,
    /,
    *,
    default_validators: list[str] | None = None,
) -> deque[Argument]:
    result = deque[Argument]()
    stack = deque[str]()
    start = None

    for i, char in enumerate(text):
        match char:
            case "<":
                start = i if not stack else start
                stack.append("<")
            case ">" if stack:
                stack.pop()
                if not stack and start is not None:
                    node = text[start : i + 1]
                    name = parse_argument_name(node) or text[start + 1 : i]
                    nested = Syntax.REGEX.check(name) or "<" in name and ">" in name
                    argument = Argument(node, name, nested)
                    result.append(
                        parse_validated_argument(argument)
                        if not default_validators
                        else parse_default_validated_argument(argument, default_validators),
                    )
            case _:
                pass

    return result


def parse_argument_name(argument_node: str, /) -> str | None:
    if (arg_name := ARG_NAME.match(argument_node)) is not None:
        return arg_name.group(1)

    return None


def parse_argument_names(arguments: Iterable[Argument], /) -> list[str]:
    return [parse_argument_name(argument.node) or argument.name for argument in arguments]


def parse_validated_argument(argument: Argument, /) -> Argument:
    if not argument.nested and (m := VALIDATED_ARGS.search(argument.node)) is not None:
        argument.name = m.group(1)

    return argument


def parse_default_validated_argument(argument: Argument, default_validators: list[str], /) -> Argument:
    if not argument.nested:
        argument.node = f"{argument.node[:-1]}:{':'.join(default_validators)}>"

    return argument


def parse_validated_arguments(arguments: Iterable[Argument], /) -> list[Argument]:
    for argument in arguments:
        parse_validated_argument(argument)

    return list(arguments)


def parse_default_validated_arguments(arguments: Iterable[Argument], default_validators: list[str], /) -> list[Argument]:
    for argument in arguments:
        parse_default_validated_argument(argument, default_validators)

    return list(arguments)


@dataclasses.dataclass
class Argument:
    node: str
    name: str
    nested: bool


__all__ = (
    "Argument",
    "parse_argument_name",
    "parse_argument_names",
    "parse_arguments",
    "parse_default_validated_arguments",
    "parse_validated_arguments",
)
