from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["EmptyFileError"]


class EmptyFileError(Exception):
    DefaultMessage: LiteralString = "Given file is empty."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
