from .abc import ABCValidator
import typing
import re


class IntValidator(ABCValidator):
    """ Check if value can be formally converted to integer """

    key = "int"

    def check(self, value: str, *args) -> typing.Optional[typing.Union[int, typing.List[int]]]:
        if not isinstance(value, list) and value.isdigit():
            return int(value)
        elif isinstance(value, list):
            int_list = []
            for v in value:
                if not v.isdigit():
                    return
                int_list.append(int(v))
            return int_list


class FloatValidator(ABCValidator):
    """ Check if value can be formally converted to float """

    key = "float"

    def check(self, value: str, *args) -> typing.Optional[typing.Union[float, typing.List[float]]]:
        if not isinstance(value, list) and re.match(r"^-?\d+(?:\.\d+)?$", value):
            return float(value)
        elif isinstance(value, list):
            float_list = []
            for v in value:
                if not re.match(r"^-?\d+(?:\.\d+)?$", v):
                    return
                float_list.append(float(v))
            return float_list


default_validators = [IntValidator(), FloatValidator()]
