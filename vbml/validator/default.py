from .abc import ABCValidator
import typing
import re


class IntValidator(ABCValidator):
    """ Check if value can be formally converted to integer """

    key = "int"

    def check(self, value: str, *args) -> typing.Optional[int]:
        if value.isdigit():
            return int(value)


class FloatValidator(ABCValidator):
    """ Check if value can be formally converted to float """

    key = "float"

    def check(self, value: str, *args) -> typing.Optional[float]:
        if re.match(r"^-?\d+(?:\.\d+)?$", value):
            return float(value)


default_validators = [IntValidator(), FloatValidator()]
