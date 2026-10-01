class VBMLError(BaseException):
    def __init__(self, message: str, /) -> None:
        super().__init__(message)
        self.message = message


class PatternError(VBMLError):
    pass


class ParseError(VBMLError):
    pass


__all__ = ("ParseError", "PatternError", "VBMLError")
