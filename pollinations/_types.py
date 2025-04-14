from PIL import Image
from httpx import URL, Client, AsyncClient, Response  # noqa: F401

from typing import (
    Any,
    Type,
    TypeVar,
    List,
    Tuple,
    Optional,
    TypedDict,
    Union,
    Dict,
    Iterator,
    AsyncIterator,
    Callable,
)  # noqa: F401


__all__ = [
    "Image",
    "Any",
    "Type",
    "TypeVar",
    "List",
    "Tuple",
    "Optional",
    "TypedDict",
    "Union",
    "Dict",
    "Iterator",
    "AsyncIterator",
    "Callable",
    "URL",
    "Client",
    "AsyncClient",
    "Response",
    "Info",
]


class Info:
    class TextModel(TypedDict, total=False):
        name: str
        description: str
        provider: str
        input_modalities: List[str]
        output_modalities: List[str]
        vision: bool
        audio: bool
        uncensored: Optional[bool]
        reasoning: Optional[bool]
        aliases: Optional[str]
        voices: Optional[List[str]]

    class ImageModel(TypedDict):
        name: str
