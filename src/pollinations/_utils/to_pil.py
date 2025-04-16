from ..types import ImageData, PILImage, Args, Kwargs

from io import BytesIO
from PIL import Image

__all__: list[str] = ["_to_pil"]

def _to_pil(data: ImageData, *args: Args, **kwargs: Kwargs) -> PILImage:
    return Image.open(data if isinstance(data, BytesIO) else BytesIO(data))
