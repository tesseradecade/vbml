from vbml.patcher.abc import ABCPatcher
from vbml.pattern import Pattern


class Patcher(ABCPatcher):
    def check(self, text: str, pattern: Pattern, ignore_validation: bool = False):
        pass
