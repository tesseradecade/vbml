from __future__ import annotations

import dataclasses
import re
import typing
from collections import deque
from collections.abc import Iterable

from vbml.parser.syntax import Syntax

ARG_NAME: typing.Final[re.Pattern[str]] = re.compile(r"<\(.*\)([A-Za-z0-9_" + "".join(Syntax) + r"]*)\s*>", re.MULTILINE)
VALIDATED_ARGS: typing.Final[re.Pattern[str]] = re.compile(r"<\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*[^>]+?>", re.MULTILINE)


def parse_arguments(text: str, /) -> deque[Argument]:
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
                    name = text[start + 1 : i]
                    result.append(Argument(text[start : i + 1], name, nested="<" in name and ">" in name))
            case _:
                pass

    return result


def parse_argument_names(arguments: Iterable[Argument], /) -> list[str]:
    result = list[str]()

    for argument in arguments:
        if (arg_name := ARG_NAME.match(argument.node)) is not None:
            argument.name = arg_name.group(1)

        result.append(argument.name)

    return result


def parse_validated_arguments(arguments: Iterable[Argument], /) -> list[Argument]:
    for argument in arguments:
        if not argument.nested and (m := VALIDATED_ARGS.search(argument.node)) is not None:
            argument.name = m.group(1)

    return list(arguments)


def parse_default_validated_arguments(
    arguments: Iterable[Argument],
    default_validators: list[str],
) -> list[Argument]:
    for argument in arguments:
        if not argument.nested:
            argument.node = f"{argument.node[:-1]}:{':'.join(default_validators)}>"

    return list(arguments)


@dataclasses.dataclass
class Argument:
    node: str
    name: str
    nested: bool


__all__ = (
    "Argument",
    "parse_argument_names",
    "parse_arguments",
    "parse_default_validated_arguments",
    "parse_validated_arguments",
)
