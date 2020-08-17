from dataclasses import dataclass
import typing


@dataclass
class SyntaxArgument:
    name: str
    index: int
    inclusion: typing.Optional[str]


@dataclass
class RecursionArgument:
    value: str
    create_pattern_data: dict


@dataclass
class Validator:
    validation: dict
    nested: dict
