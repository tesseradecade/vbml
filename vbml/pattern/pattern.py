from __future__ import annotations

import re
import typing

from vbml.error import ParseError, VBMLError
from vbml.parser.parser import parse
from vbml.pattern.abc import ABCPattern
from vbml.validator.ahead import AheadValidation, RecursionArgument, Validator

if typing.TYPE_CHECKING:
    from vbml.parser.validator_parser import ArgumentName, Nesting, ValidatorName

type Inclusion = str

DEFAULT_REGEX: typing.Final[str] = "{}$"
DEFAULT_REPR_NOUN: typing.Final[str] = "?"


class Pattern(ABCPattern):
    _representation: str | None
    pregmatch: dict[str, typing.Any] | None

    __slots__ = (
        "pattern",
        "flags",
        "compiler",
        "validators",
        "validation",
        "nestings",
        "recursions",
        "inclusions",
        "ahead",
        "text",
        "regex",
        "lazy",
        "repr_noun",
        "arguments",
        "pregmatch",
        "_representation",
    )

    def __init__(
        self,
        text: str,
        regex: str = DEFAULT_REGEX,
        lazy: bool = True,
        flags: re.RegexFlag | None = None,
        default_validators: list[ValidatorName] | None = None,
        nestings: dict[ValidatorName, Nesting] | None = None,
        *,
        inclusions: dict[ArgumentName, Inclusion | None] | None = None,
        repr_noun: str = DEFAULT_REPR_NOUN,
        **context: typing.Any,
    ) -> None:
        self.pattern = (
            parse(
                text,
                lazy=lazy,
                default_validators=default_validators,
                nestings=nestings,
            )
            .map_err(lambda error: VBMLError(error))
            .unwrap()
        )
        self.flags = flags or re.NOFLAG
        self.compiler = re.compile(regex.format(self.pattern.pattern), self.flags)

        self.validators = list(
            map(
                lambda validator: Validator(validator.argument, validator.validation, validator.nestings),
                self.pattern.validators,
            ),
        )
        self.validation = {validator.name: validator.validation for validator in self.validators}
        self.nestings = [nested for validator in self.validators for nested in validator.nested.values()]
        self.recursions = {
            argument: RecursionArgument(value=pattern.pattern, create_pattern_data=pattern.data)
            for argument, pattern in self.pattern.recursion_patterns.items()
        }
        self.inclusions = {argument: inclusion.unwrap_or_none() for argument, inclusion in self.pattern.inclusions.items()}

        self.ahead = AheadValidation(type(self), self.inclusions, self.nestings, self.recursions)
        self.text = text
        self.regex = regex
        self.lazy = lazy
        self.repr_noun = repr_noun
        self.arguments = self.pattern.arguments
        self.pregmatch = None
        self._representation = None

    def __repr__(self) -> str:
        return "<{}: text={!r}, regex={!r}, flags={!r}, lazy={!r}, pregmatch={!r}>".format(
            ".".join((type(self).__module__, type(self).__name__)),
            self.text,
            self.regex,
            self.flags,
            self.lazy,
            self.pregmatch,
        )

    @property
    def representation(self) -> str:
        if self._representation is None:
            self._representation = self.text

            for argument in self.pattern.arguments:
                self._representation = self._representation.replace(argument.node, self.repr_noun)

        return self._representation

    def parse(self, text: str) -> bool:
        if not text:
            return False

        match = self.compiler.match(text)
        if match is None:
            return False

        self.pregmatch = pregmatch = self.ahead.get_groupdict(match)
        return pregmatch is not None

    def dict(self) -> dict[str, typing.Any]:
        if self.pregmatch is None:
            raise ParseError("Not matched or failed.")
        return self.pregmatch


__all__ = ("Pattern",)
