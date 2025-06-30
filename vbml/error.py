class VBMLError(BaseException):
    pass


class PatternError(VBMLError):
    pass


class ParseError(VBMLError):
    pass


__all__ = ("ParseError", "PatternError", "VBMLError")
