from .read_image import _read_image
from ..types import Filename, ImageFormat, Args, Kwargs

from typing import Optional
from base64 import b64encode

__all__: list[str] = ["_format_image"]


def _format_image(
    file: Filename, *args: Args, **kwargs: Kwargs
) -> Optional[ImageFormat]:
    image_content = _read_image(file, *args, **kwargs)
    if image_content is None:
        return None

    encoded_image = b64encode(image_content.getvalue()).decode("utf-8")
    extensions = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
    }

    extension = extensions.get(file.split(".")[-1].lower(), "image/jpeg")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{extension};base64,{encoded_image}"},
    }
