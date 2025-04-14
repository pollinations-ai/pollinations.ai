import os
import io
import base64

from pollinations._types import Optional, Union, Image


def _safe_check(file_path: str) -> bool:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    if not os.path.isfile(file_path):
        raise ValueError(f"{file_path} is not a file.")
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read {file_path}. Bad permissions.")
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"{file_path} is empty.")
    return True


def _read_image(file_path: str) -> Optional[io.BytesIO]:
    _safe_check(file_path)
    with open(file_path, "rb") as f:
        return io.BytesIO(f.read())


def _format_image(file_path: str) -> Optional[dict[str, Union[str, dict[str, str]]]]:
    image_content = _read_image(file_path)
    if image_content is None:
        return None

    file_ext = file_path.split(".")[-1].lower()
    encoded_image = base64.b64encode(image_content.getvalue()).decode("utf-8")

    mtypes: dict[str, str] = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
    }

    mtype = mtypes.get(file_ext, "image/jpeg")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{mtype};base64,{encoded_image}"},
    }


def _read_image_content(content: bytes) -> bytes:
    # added this just incase I need to update it later
    if not content:
        raise ValueError("Image content is empty.")
    return content


async def _read_image_content_async(content: bytes) -> bytes:
    # added this just incase I need to update it later
    if not content:
        raise ValueError("Async image content is empty.")
    return content


def _to_pil(image_data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_data))
