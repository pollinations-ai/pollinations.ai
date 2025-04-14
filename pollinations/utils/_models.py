import httpx

from pollinations._types import List, Info
from pollinations._constants import TEXT_API_URI, IMAGE_API_URI

__all__ = ["text_models", "image_models"]


def _get_models(client: httpx.Client) -> List[Info.TextModel | Info.ImageModel]:
    response = client.get("/models")
    response.raise_for_status()
    return response.json()


def text_models() -> List[Info.TextModel | Info.ImageModel]:
    return _get_models(httpx.Client(base_url=TEXT_API_URI))


def image_models() -> List[Info.TextModel | Info.ImageModel]:
    return _get_models(httpx.Client(base_url=IMAGE_API_URI))
