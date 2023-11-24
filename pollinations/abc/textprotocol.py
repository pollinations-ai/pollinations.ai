"""
pollinations.abc.imageprotocol

Classes:
    TextProtocol: Text protocol for the TextObject class.
"""

from typing import Protocol


class TextProtocol(Protocol):
    """
    TextProtocol: Text protocol for the TextObject class.
    """

    prompt: str
    response: str
