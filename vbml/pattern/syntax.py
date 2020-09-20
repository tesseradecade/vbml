""" VBML Syntax constants
UNION - splits value afterwards with given inclusion
ONE_CHAR - every symbol of inclusion is possible char to be taken
EXCEPT - approve value if it doesnt contain any symbol from inclusion
REGEX - inclusion is regex
RECURSION - schema inside the inclusion creates new pattern
"""

from typing import Tuple
from re import compile
import re

# Syntax Chars

UNION = "*"
ONE_CHAR = "^"
EXCEPT = "#"
REGEX = "$"
IGNORE = "!"
RECURSION = "&"
ANYTHING = "1"


# Constants

SYNTAX_CHARS: Tuple[str, ...] = (UNION, ONE_CHAR, EXCEPT, REGEX, IGNORE, RECURSION, ANYTHING)
ESCAPE = {ord(x): "\\" + x for x in r"\.*+?()[]|^${}&"}

# Regex patterns

ARGUMENT = r"<\1>"
ARGS_FINDALL = compile(r"(<(.*?)>)", re.MULTILINE)
ARGS_NAME_FINDALL = compile(r"<(.*?)>", re.MULTILINE)
TYPED_ARGS_FINDALL = compile(r"(<.*?([a-zA-Z0-9_]+):.*?>)", re.MULTILINE)
ARGS_DELETE = compile(r"<(.*?)(?::[\[\]a-zA-Z_0-9, ]+)+>", re.MULTILINE)
INCLUSION_DELETE = compile(r"<(?:\(.*?\))(.*?)>", re.MULTILINE)
VALIDATORS_FINDALL = compile(r":([a-zA-Z0-9_, ]+|[\[]+[a-zA-Z0-9_, ]+[\]]+)", re.MULTILINE)
