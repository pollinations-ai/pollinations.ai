from ..types import Prompt, System, Args, Kwargs

from urllib.parse import quote

__all__: list[str] = ["_encode_string"]


def _encode_string(string: Prompt | System, *args: Args, **kwargs: Kwargs) -> str:
    return quote(string)
