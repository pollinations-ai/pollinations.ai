from .check_file import _check_file
from ..types import Filename, ImageData, Args, Kwargs

from io import BytesIO

__all__: list[str] = ["_read_image"]


def _read_image(file: Filename, *args: Args, **kwargs: Kwargs) -> ImageData:
    _check_file(file)

    with open(file, "rb") as f:
        return BytesIO(f.read())
