import typing
from vbml.pattern.syntax import UNION, RECURSION
from vbml.utils.syntax_argument import RecursionArgument, Validator

if typing.TYPE_CHECKING:
    from vbml.pattern.abc import ABCPattern


class AheadValidation:
    def __init__(
        self,
        pattern: "ABCPattern",
        inclusions: typing.Dict[str, typing.Optional[str]],
        validators: typing.List[Validator],
        recursions: typing.Dict[str, RecursionArgument],
    ):
        self.inclusions = inclusions
        self.recursions = recursions
        self.validators = validators
        self.pattern: typing.Type["ABCPattern"] = type(pattern)

    def get_groupdict(self, match) -> typing.Union[dict, None]:
        groupdict: dict = match.groupdict()

        for inclusion in self.inclusions:
            if inclusion.startswith(UNION):
                union_name = inclusion.strip(UNION)
                groupdict[union_name] = [
                    argument
                    for argument in groupdict[union_name].split(self.inclusions[inclusion][0])
                    if argument
                ]
            elif inclusion.startswith(RECURSION):
                name = inclusion.strip(RECURSION)
                pattern = self.pattern(**self.recursions[inclusion].create_pattern_data)
                if pattern.parse(groupdict[name]):
                    groupdict.update({name: pattern.dict()})
                else:
                    return

        [
            groupdict.update(self.validators[validator].nested[nested](groupdict) or {})
            for validator in self.validators
            for nested in validator.nested
        ]
        return groupdict
