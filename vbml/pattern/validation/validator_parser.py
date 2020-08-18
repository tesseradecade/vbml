import typing
import re
from vbml.utils import Validator
from vbml.pattern.syntax import VALIDATORS_FINDALL, SYNTAX_CHARS
from vbml.utils import PatternError, flatten

VALIDATOR_ARGUMENT = r"\[(.+)+\]"


def get_validators(
    validated_arguments: typing.List[typing.Tuple[str, str]],
    impl_nestings: typing.Optional[typing.Dict[str, typing.Callable[[str], typing.Any]]] = None,
) -> typing.List[Validator]:
    """ Get validators from validated arguments including validator's arguments
    :param validated_arguments: [(argument_full_pattern, selected_argument_name), ...]
    :param impl_nestings: post validators called nestings derived to the pattern
    :return: list of validators
    """

    if not impl_nestings:
        impl_nestings = {}

    new_validators = []

    for argument_full in validated_arguments:
        argument_node, argument_name = argument_full
        validators: typing.List[str] = re.findall(VALIDATORS_FINDALL, argument_node)

        # Get validator's arguments
        for validator in validators:
            nested: dict = {}
            validated: dict = {}

            # Nesting validator
            if validator.startswith("[") and validator.endswith("]"):
                nestings = validator.strip("[ ]").split(",")
                for nesting in nestings:
                    if nesting not in impl_nestings:
                        raise PatternError(f"{nesting!r} is undefined in implemented nestings")
                    nested[nesting] = impl_nestings[nesting]
            # Validated
            else:
                arguments = flatten(
                    [
                        argument.split(",")
                        for argument in re.findall(
                            f":{validator}{VALIDATOR_ARGUMENT}", argument_node
                        )
                    ]
                )
                validated[validator] = arguments

            new_validators.append(Validator(argument_name, validated, nested))
    return new_validators


def get_inclusion(argument: str) -> typing.Optional[str]:
    """ Get inclusion from argument
    :param argument: raw argument
    :return: Optional[inclusion]
    """
    inclusion_list: typing.List[str] = re.findall(
        r"^\((.*?)\)[a-zA-Z0-9_" + "".join(SYNTAX_CHARS) + "]+[:]?.*?$", argument
    )

    if inclusion_list:
        inclusion: str = inclusion_list[0].replace("\\n", "\n")
        return inclusion
    return None


def add_inclusion(inclusions: dict, group_dict: dict) -> typing.Dict[str, str]:
    """ Add inclusion as prefix """
    for argument in group_dict:
        if inclusions.get(argument) is not None:
            group_dict[argument] = inclusions[argument] + group_dict[argument]
    return group_dict
