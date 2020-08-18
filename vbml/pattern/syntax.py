from typing import Tuple
from re import compile
import re

# Arg-type syntax

UNION = "*"
ONE_CHAR = "^"
EXCEPT = "#"
REGEX = "$"
IGNORE = "!"
RECURSION = "&"

# Constants

SYNTAX_CHARS: Tuple[str, ...] = (UNION, ONE_CHAR, EXCEPT, REGEX, IGNORE, RECURSION)
ESCAPE = {ord(x): "\\" + x for x in r"\.*+?()[]|^${}&"}

# Regex patterns

ARGUMENT = r"<\1>"
ARGS_FINDALL = compile(r"(<(.*?)>)", re.MULTILINE)
ARGS_NAME_FINDALL = compile(r"<(.*?)>", re.MULTILINE)
TYPED_ARGS_FINDALL = compile(r"(<.*?([a-zA-Z0-9_]+):.*?>)", re.MULTILINE)
ARGS_DELETE = compile(r"<(.*?)(?::[\[\]a-zA-Z_0-9, ]+)+>", re.MULTILINE)
INCLUSION_DELETE = compile(r"<(?:\(.*?\))(.*?)>", re.MULTILINE)
VALIDATORS_FINDALL = compile(r":([a-zA-Z0-9_, ]+|[\[]+[a-zA-Z0-9_, ]+[\]]+)", re.MULTILINE)
