from vbml.pattern.abc import ABCPattern
from vbml.pattern import syntax
from vbml.pattern.syntax_processing import Syntax
from vbml.pattern.validation import get_validators, get_inclusion, AheadValidation
from vbml.utils import PatternError, ParseError, SyntaxArgument, RecursionArgument
import typing
import re


class Pattern(ABCPattern):
    """ Main patcher to parse and validate
    Pattern documentation: https://github.com/tesseradecade/vbml/blob/master/docs/pattern.md
    """

    def __init__(
        self,
        text: str,
        regex: str = "{}$",
        lazy: bool = True,
        flags: typing.Optional[re.RegexFlag] = None,
        default_validators: typing.Optional[typing.List[str]] = None,
        nestings: typing.Optional[typing.Dict[str, typing.Callable[[str], typing.Any]]] = None,
        **context,
    ):
        super().__init__(text, regex, lazy)

        self.syntax = Syntax()
        self.text = text
        self.regex = regex
        self.lazy = lazy

        context["flags"] = flags
        context["default_validators"] = default_validators
        context["nestings"] = nestings

        # Find all validated arguments
        validated_arguments: typing.List[typing.Tuple[str, str]]

        if context["default_validators"] is not None:
            validated_arguments = [
                (arg[0][0:-1] + ":" + ":".join(context["default_validators"]) + ">", arg[1])
                for arg in syntax.ARGS_FINDALL.findall(text)
            ]
        else:
            validated_arguments = syntax.TYPED_ARGS_FINDALL.findall(text)

        # Parse arguments and save validators
        self.validators = get_validators(validated_arguments, nestings)
        self.validation = {p.name: p.validation for p in self.validators}

        # Delete arguments from text
        text = syntax.ARGS_DELETE.sub(syntax.ARGUMENT, text)

        # Save inclusion from text
        inclusions: typing.List[typing.Optional[str]] = context.get("inclusions") or [
            get_inclusion(argument) for argument in re.findall(syntax.ARGS_NAME_FINDALL, text)
        ]

        # Delete inclusion from text
        text = syntax.INCLUSION_DELETE.sub(syntax.ARGUMENT, text)

        # Add representation
        self.representation: str = re.sub(
            syntax.ARGS_NAME_FINDALL, context.get("repr_noun", "?"), text
        )

        self.arguments: typing.List[str] = re.findall(syntax.ARGS_NAME_FINDALL, text)
        self.inclusions = dict(zip(self.arguments, inclusions))
        self.recursions: typing.Dict[str, RecursionArgument] = {}

        # Add escape symbols
        text = text.translate(syntax.ESCAPE)

        # Reveal arguments
        for i, argument in enumerate(self.arguments):
            syntax_argument = SyntaxArgument(argument, i, self.inclusions.get(argument))

            if not argument:
                raise PatternError("Argument cannot be empty")
            elif argument.startswith(syntax.RECURSION):
                self.recursions[argument] = self.syntax.recursion_arg(syntax_argument)
                print(self.recursions)

            if argument[0] in syntax.SYNTAX_CHARS:
                text = text.replace(
                    "<{}>".format(argument.translate(syntax.ESCAPE)),
                    self.syntax.get_syntax(argument[0])(self.syntax, syntax_argument),
                )
            else:
                pre = self.inclusions.get(argument) or ""
                text = text.replace(
                    f"<{argument}>", f"(?P<{argument}>{pre}.*{'?' if lazy else ''})"
                )

        self.compiler = re.compile(regex.format(text), flags=context.get("flags") or 0)
        self.pregmatch: typing.Optional[dict] = None
        self.ahead = AheadValidation(Pattern, self.inclusions, self.validators, self.recursions)

    def parse(self, text: str) -> typing.Optional[bool]:
        if not text:
            return False

        match = self.compiler.match(text)
        if match is None:
            return False

        self.pregmatch = self.ahead.get_groupdict(match)
        return self.pregmatch is not None

    def dict(self) -> dict:
        if self.pregmatch is None:
            raise ParseError("Not matched or failed")
        return self.pregmatch
