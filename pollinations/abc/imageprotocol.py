"""
pollinations.abc.imageprotocol

Classes:
    ImageProtocol: Image protocol for the ImageObject class.
"""

from typing import Protocol


class ImageProtocol(Protocol):
    """
    ImageProtocol: Image protocol for the ImageObject class.
    """

    prompt: str
    url: str
    date: str
    content: bin
