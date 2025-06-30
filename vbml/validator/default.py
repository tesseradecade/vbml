import re
import typing

from vbml.validator.abc import ABCValidator

NEGATIVE_INT: typing.Final[re.Pattern[str]] = re.compile(r"^-\d+$")
FLOAT: typing.Final[re.Pattern[str]] = re.compile(r"^(?:\d+\.\d+|\.\d+)?$")
NEGATIVE_FLOAT: typing.Final[re.Pattern[str]] = re.compile(r"^-(?:\d+\.\d+|\.\d+)?$")
BOOLEAN: typing.Final[re.Pattern[str]] = re.compile(r"^(?i:true|false)$")


class IntValidator(ABCValidator):
    key = "int"

    def check(self, value: str | list[str], *args: str) -> int | list[int] | None:
        if not isinstance(value, list) and value.isdigit():
            return int(value)

        if isinstance(value, list):
            int_list = list[int]()
            for v in value:
                if not v.isdigit():
                    return None
                int_list.append(int(v))

            return int_list

        return None


class NegativeIntValidator(ABCValidator):
    key = "neg_int"

    def check(self, value: str | list[str], *args: str) -> int | list[int] | None:
        if not isinstance(value, list) and NEGATIVE_INT.fullmatch(value) is not None:
            return int(value)

        if isinstance(value, list):
            int_list = list[int]()
            for v in value:
                if NEGATIVE_INT.fullmatch(v) is None:
                    return None
                int_list.append(int(v))

            return int_list

        return None


class FloatValidator(ABCValidator):
    key = "float"

    def check(self, value: str | list[str], *args: str) -> float | list[float] | None:
        if not isinstance(value, list) and FLOAT.match(value) is not None:
            return float(value)

        if isinstance(value, list):
            float_list = list[float]()
            for v in value:
                if FLOAT.match(v) is None:
                    return None
                float_list.append(float(v))

            return float_list

        return None


class NegativeFloatValidator(ABCValidator):
    key = "neg_float"

    def check(self, value: str | list[str], *args: str) -> float | list[float] | None:
        if not isinstance(value, list) and NEGATIVE_FLOAT.match(value) is not None:
            return float(value)

        if isinstance(value, list):
            float_list = list[float]()
            for v in value:
                if NEGATIVE_FLOAT.match(v) is None:
                    return None
                float_list.append(float(v))

            return float_list

        return None


class BoolValidator(ABCValidator):
    key = "bool"
    bool_map = {"True": True, "False": False}

    def check(self, value: str | list[str], *args: str) -> bool | list[bool] | None:
        if not isinstance(value, list) and BOOLEAN.match(value) is not None:
            return self.bool_map.get(value.capitalize())

        if isinstance(value, list):
            bool_list = list[bool]()
            for v in value:
                if BOOLEAN.match(v) is None or (boolean := self.bool_map.get(v.capitalize())) is None:
                    return None
                bool_list.append(boolean)

            return bool_list

        return None


default_validators: typing.Final = (
    BoolValidator(),
    IntValidator(),
    NegativeIntValidator(),
    FloatValidator(),
    NegativeFloatValidator(),
)


__all__ = (
    "BoolValidator",
    "FloatValidator",
    "IntValidator",
    "NegativeFloatValidator",
    "NegativeIntValidator",
    "default_validators",
)
