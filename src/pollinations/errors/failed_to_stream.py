from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["FailedToStreamError"]


class FailedToStreamError(Exception):
    DefaultMessage: LiteralString = "Failed to stream text."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
