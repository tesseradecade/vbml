from __future__ import annotations

import dataclasses
import enum
import typing
from collections.abc import Callable
from functools import cached_property, wraps

from fntypes.library.monad.option import Nothing, Option, Some
from fntypes.library.monad.result import Error, Ok, Result

type SyntaxResult = Result[SyntaxPattern, str]
type SyntaxHandler = Callable[[Argument], SyntaxResult]

ESCAPE_TABLE: typing.Final = {ord(x): "\\" + x for x in r"/\.*+?()[]|^${}&"}


def escape(string: str, /) -> str:
    return string.translate(ESCAPE_TABLE)


def syntax[F: SyntaxHandler](
    synt: Syntax,
    /,
    *,
    require_name: bool = False,
    require_inclusion: bool = False,
) -> Callable[[F], F]:
    def decorator(func: F, /) -> F:
        @wraps(wrapped=func)
        def wrapper(argument: Argument, /) -> SyntaxResult:
            argument_name = argument.name.unwrap_or("").removeprefix(synt)
            inclusion = argument.inclusion.unwrap_or("")

            if not any((require_name, require_inclusion)) and any((argument_name, inclusion)):
                return Error(f"Inclusion and name in {synt.name.lower()}-argument are forbidden.")

            if require_name and not argument_name:
                return Error(f"`{synt.name.lower()}` argument should be named.")

            if require_inclusion and not inclusion:
                return Error(f"`{synt.name.lower()}` argument must include at least one symbol in its inclusion.")

            return func(argument)

        synt.__dict__.update(dict(handler=wrapper))
        return typing.cast("F", wrapper)

    return decorator


@enum.unique
class Syntax(str, enum.Enum):
    UNION = "*"
    """Splits the value using the given inclusion."""

    SINGLE = "^"
    """Any single character from the inclusion is an allowed character."""

    EXCEPT = "#"
    """Accepts the value if it does not contain any character from the inclusion."""

    REGEX = "$"
    """The inclusion is treated as a regular expression."""

    RECURSION = "&"
    """The schema inside the inclusion defines a new pattern."""

    ANY = "1"
    """Any characters are allowed, except the empty character."""

    IGNORE = "!"
    """Ignore any characters, include the empty character."""

    def __call__(self, argument: Argument, /) -> SyntaxResult:
        return self.handler(argument)

    @cached_property
    def handler(self) -> SyntaxHandler:
        # typed alternative to getting self.__dict__["handler"]
        # if key "handler" is not found in self.__dict__, raises NotImplementedError
        raise NotImplementedError(f"Syntax handler is not implemented for {self!r}")


@dataclasses.dataclass(slots=True, frozen=True)
class SyntaxPattern:
    pattern: str
    syntax: Syntax
    data: dict[str, typing.Any] = dataclasses.field(default_factory=lambda: dict[str, typing.Any]())


@dataclasses.dataclass(slots=True, frozen=True)
class Argument:
    name: Option[str] = dataclasses.field(default_factory=Nothing)
    inclusion: Option[str] = dataclasses.field(default_factory=Nothing)


@syntax(Syntax.UNION, require_name=True)
def union_syntax(argument: Argument) -> SyntaxResult:
    return Ok(SyntaxPattern("(?P<" + argument.name.unwrap().removeprefix(Syntax.UNION) + ">.*)", Syntax.UNION))


@syntax(Syntax.SINGLE, require_name=True)
def single_syntax(argument: Argument) -> SyntaxResult:
    match argument.inclusion:
        case Some(inclusion):
            pattern = "[" + inclusion.translate(ESCAPE_TABLE) + "]"
        case _:
            pattern = "."

    return Ok(SyntaxPattern("(?P<{}>{})".format(argument.name.unwrap().removeprefix(Syntax.SINGLE), pattern), Syntax.SINGLE))


@syntax(Syntax.EXCEPT, require_name=True, require_inclusion=True)
def except_syntax(argument: Argument) -> SyntaxResult:
    pattern = "(?P<{}>{}+)".format(
        argument.name.unwrap().removeprefix(Syntax.EXCEPT),
        "[^" + argument.inclusion.unwrap().translate(ESCAPE_TABLE) + "]",
    )
    return Ok(SyntaxPattern(pattern, Syntax.EXCEPT))


@syntax(Syntax.REGEX, require_inclusion=True)
def regex_syntax(argument: Argument) -> SyntaxResult:
    return Ok(SyntaxPattern(argument.inclusion.unwrap(), Syntax.REGEX))


@syntax(Syntax.ANY)
def any_syntax(_: Argument) -> SyntaxResult:
    return Ok(SyntaxPattern("(?:.+)", Syntax.ANY))


@syntax(Syntax.IGNORE)
def ignore_syntax(_: Argument) -> SyntaxResult:
    return Ok(SyntaxPattern("(?:.*?)", Syntax.IGNORE))


@syntax(Syntax.RECURSION, require_name=True, require_inclusion=True)
def recursion_syntax(argument: Argument) -> SyntaxResult:
    return Ok(
        SyntaxPattern(
            "(?P<{}>.*)".format(argument.name.unwrap().removeprefix(Syntax.RECURSION)),
            Syntax.RECURSION,
            data=dict(text=argument.inclusion.unwrap().strip('"')),
        ),
    )


SYNTAX_MAP: typing.Final = {syntax.value: syntax for syntax in Syntax}


__all__ = ("Argument", "SYNTAX_MAP", "Syntax", "SyntaxPattern", "escape", "syntax")
