from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["InvalidOrUnknownPromptError"]


class InvalidOrUnknownPromptError(Exception):
    DefaultMessage: LiteralString = "Prompt was invalid, none, or could not be found."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
