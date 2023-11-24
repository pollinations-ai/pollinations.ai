from typing import Protocol


class ImageProtocol(Protocol):
    prompt: str
    url: str
    date: str
    content: bin
