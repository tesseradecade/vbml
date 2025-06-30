import re
import typing

from fntypes.library.monad.option import Nothing, Option, Some

from vbml.parser.argument_parser import Argument
from vbml.parser.syntax import Syntax

ARGUMENT: typing.Final[str] = r"<\1>"
INCLUSION: typing.Final[re.Pattern[str]] = re.compile(r"^\((.*?)\)[a-zA-Z0-9_" + "".join(Syntax) + r"]+[:]?.*?$", re.MULTILINE)
INCLUSION_NESTED: typing.Final[re.Pattern[str]] = re.compile(r"^\((.*)\)[a-zA-Z0-9_" + "".join(Syntax) + r"]+[:]?.*$", re.MULTILINE)


def parse_inclusion(argument: Argument, /) -> Option[str]:
    inclusion_list: list[str] = (INCLUSION_NESTED if argument.nested else INCLUSION).findall(argument.node.strip("<>"))
    return Nothing() if not inclusion_list else Some(inclusion_list[0].replace("\\n", "\n"))


__all__ = ("parse_inclusion",)
