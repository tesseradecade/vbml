"""Markup language that compiles to regex.

Exmaple::

    from vbml import Patcher, Pattern

    patcher = Patcher()
    pattern = Pattern("I have <amount:int> apples. They are <adj>")

    result1 = patcher.check(pattern, "I have 3 apples. They are green")
    result2 = patcher.check(pattern, "I have three apples. They are green")
    result3 = patcher.check(pattern, "I have apples")

    result1  # {"amount": 3, "adj": "green"}
    result2  # None
    result3  # False
"""

from vbml.patcher.abc import ABCPatcher
from vbml.patcher.patcher import Patcher
from vbml.pattern.abc import ABCPattern
from vbml.pattern.pattern import Pattern
from vbml.validator.abc import ABCValidator, ValidatorResult
from vbml.validator.ahead import AheadValidation, RecursionArgument, Validator
from vbml.validator.default import BoolValidator, FloatValidator, IntValidator, NegativeFloatValidator, NegativeIntValidator
from vbml.validator.func import FuncBasedValidator, FuncBasedValidatorCallable
from vbml.validator.map import ValidatorsMap

__all__ = (
    "ABCPatcher",
    "ABCPattern",
    "ABCValidator",
    "AheadValidation",
    "BoolValidator",
    "FloatValidator",
    "FuncBasedValidator",
    "FuncBasedValidatorCallable",
    "IntValidator",
    "NegativeFloatValidator",
    "NegativeIntValidator",
    "Patcher",
    "Pattern",
    "RecursionArgument",
    "Validator",
    "ValidatorResult",
    "ValidatorsMap",
)
