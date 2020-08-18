import typing
from vbml.pattern.syntax import UNION, RECURSION
from vbml.utils.syntax_argument import RecursionArgument, Validator

if typing.TYPE_CHECKING:
    from vbml.pattern import Pattern


class AheadValidation:
    """ Ahead validator. The single specific validator used in Pattern
    Read the docs here: https://github.com/tesseradecade/vbml/blob/master/docs/pattern.md
    """

    def __init__(
        self,
        pattern: typing.Type["Pattern"],
        inclusions: typing.Dict[str, typing.Optional[str]],
        validators: typing.List[Validator],
        recursions: typing.Dict[str, RecursionArgument],
    ):
        """ Init AheadValidation
        :param pattern: Pattern type / for custom patterns
        :param inclusions: {argument: inclusion}
        :param validators: validators
        :param recursions: {argument: RecursionArgument}
        """
        self.inclusions = inclusions
        self.recursions = recursions
        self.validators = validators
        self.pattern = pattern

    def get_groupdict(self, match) -> typing.Optional[dict]:
        """ Update regex-match groupdict with the ahead validation
        :param match: regex match
        :return: updated groupdict
        """
        groupdict: dict = match.groupdict()

        for inclusion in self.inclusions:
            if inclusion.startswith(UNION):
                union_name = inclusion.strip(UNION)
                groupdict[union_name] = [
                    argument
                    for argument in groupdict[union_name].split(self.inclusions[inclusion])
                    if argument
                ]
            elif inclusion.startswith(RECURSION):
                name = inclusion.strip(RECURSION)
                pattern = self.pattern(**self.recursions[inclusion].create_pattern_data)
                if pattern.parse(groupdict[name]):
                    groupdict.update({name: pattern.dict()})
                else:
                    return None

        [
            groupdict.update(
                self.validators[validator].nested[nested](groupdict) or {}  # type: ignore
            )
            for validator in self.validators
            for nested in validator.nested
        ]
        return groupdict
