from typing import Protocol


class TextProtocol(Protocol):
    prompt: str
    response: str
