from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["FailedToTranscribeError"]


class FailedToTranscribeError(Exception):
    DefaultMessage: LiteralString = "Failed to transcribe audio."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
