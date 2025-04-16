from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["FileNotFoundError"]


class FileNotFoundError(Exception):
    DefaultMessage: LiteralString = "Could not find file."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
