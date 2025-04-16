from ..types import ErrorMessage

from typing import Self, LiteralString

__all__: list[str] = ["ImproperPermissionsError"]


class ImproperPermissionsError(Exception):
    DefaultMessage: LiteralString = "Attempted to access file with improper permissions."

    def __init__(self: Self, message: ErrorMessage) -> None:
        super().__init__(message)
