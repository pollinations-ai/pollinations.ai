from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["NotAFileError"]


class NotAFileError(Exception):
    DefaultMessage: LiteralString = "Given filename is not a file."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
