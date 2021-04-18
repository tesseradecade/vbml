from vbml.pattern.syntax import *
from vbml.utils import PatternError, SyntaxArgument, RecursionArgument
from typing import Union, NoReturn, Callable

ArgumentPattern = Union[str, NoReturn]


def syntax_for(syntax_char: str):
    """ Decorate argument shift handlers """

    def decorator(func: Callable[["Syntax", SyntaxArgument], Union[ArgumentPattern, dict]]):
        return syntax_char, func

    return decorator


class Syntax:
    """ Process argument shifts with given syntax-char
    get_syntax(syntax_char) returns shift argument handler
    Handlers are decorated with @syntax_for(syntax_char)
    """

    @syntax_for(UNION)
    def union(self, arg: SyntaxArgument) -> ArgumentPattern:
        """ UNION - splits value afterwards with given inclusion """
        if not len(arg.name.strip(UNION)):
            raise PatternError("Union argument should be named")

        pattern = "(?P<" + arg.name.strip(UNION) + ">.*)"
        return pattern

    @syntax_for(ONE_CHAR)
    def one_char(self, arg: SyntaxArgument) -> ArgumentPattern:
        """ ONE_CHAR - every symbol of inclusion is single char processed """
        if not len(arg.name.strip(ONE_CHAR)):
            raise PatternError("Char argument should be named")

        pattern = "."
        if arg.inclusion:
            # inclusions = ["\\" + inc for inc in list(inclusion[arg])]
            pattern = "[" + arg.inclusion.translate(ESCAPE) + "]"

        return "(?P<" + arg.name.strip(ONE_CHAR) + ">" + pattern + ")"

    @syntax_for(EXCEPT)
    def except_(self, arg: SyntaxArgument) -> ArgumentPattern:
        """ EXCEPT - approves value if it doesnt contain any symbol from inclusion """
        if not arg.inclusion:
            raise PatternError(
                "Except argument expression has to contain not less than one symbol in inclusion"
            )
        elif not len(arg.name.strip(EXCEPT)):
            raise PatternError("Except expression should be named")

        pattern = "[^" + arg.inclusion.translate(ESCAPE) + "]"

        return "(?P<{}>{}+)".format(arg.name.strip(EXCEPT), pattern)

    @syntax_for(REGEX)
    def regex(self, arg: SyntaxArgument) -> ArgumentPattern:
        """ REGEX - inclusion is regex """
        if not arg.inclusion:
            raise PatternError(
                "Regex argument expression has to contain not less than one symbol in inclusion"
            )
        return arg.inclusion

    @syntax_for(ANYTHING)
    def anything(self, arg: SyntaxArgument) -> ArgumentPattern:
        if arg.inclusion or arg.name.strip(ANYTHING):
            raise PatternError("Inclusion and name in anything-argument are forbidden")
        return "(?:.+)"

    @syntax_for(IGNORE)
    def ignore(self, arg: SyntaxArgument) -> ArgumentPattern:
        if arg.inclusion or arg.name.strip(IGNORE):
            raise PatternError("Inclusion and name in ignore-argument are forbidden")
        return "(?:.*?)"

    @syntax_for(RECURSION)
    def recursion(self, arg: SyntaxArgument) -> ArgumentPattern:
        """ RECURSION - schema inside the inclusion creates new pattern """
        return "(?P<" + arg.name.strip(RECURSION) + ">" + ".*" + ")"

    @staticmethod
    def recursion_arg(arg: SyntaxArgument) -> RecursionArgument:
        """ Makes inner pattern data to handle ahead of parsing """
        pattern = arg.inclusion

        # [legacy] 0.5.93
        if pattern is not None and pattern.startswith('"') and pattern.endswith('"'):
            pattern = pattern[1:-1]

        if not pattern:
            raise PatternError(
                "Recursion argument expression has to contain "
                "not less than one symbol in inclusion"
            )

        return RecursionArgument(pattern, {"text": pattern})

    def get_syntax(self, char: str) -> Callable[["Syntax", SyntaxArgument], ArgumentPattern]:
        """ Find shift argument handler by syntax char
        :param char: syntax char
        :return: shift argument handler
        """
        return {v[0]: v[1] for k, v in self.__class__.__dict__.items() if isinstance(v, tuple)}[
            char
        ]
