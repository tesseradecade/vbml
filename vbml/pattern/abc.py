from abc import ABC, abstractmethod
import typing


class ABCPattern(ABC):
    """ Vbml Pattern to parse and setup
    Read the docs here: https://github.com/tesseradecade/vbml/blob/master/docs/pattern.md
    """

    @abstractmethod
    def __init__(
        self, text: typing.Optional[str] = None, regex: str = "{}$", lazy: bool = True, **context
    ):
        """ Init Pattern
        :param text: Pattern Schema syntax
        :param regex: regex, {} is replaced with vbml pattern-generated regex
        :param lazy: https://github.com/tesseradecade/vbml/blob/master/docs/pattern.md
        :param context: dev values
        """
        pass

    @abstractmethod
    def parse(self, text: str) -> typing.Optional[bool]:
        """ Parse text with current pattern
        :param text: parsed text
        :return: did it succeed? (True/False)
        """
        pass

    @abstractmethod
    def dict(self) -> dict:
        """ Returns pregmatch or raises an exception """
        pass
