from ..types import Client, AsyncClient, TextModel, ImageModel, Args, Kwargs
from .._core import TEXT_API_URI, IMAGE_API_URI

from typing import List

__all__: list[str] = [
    "get_text_models",
    "get_image_models",
    "get_async_text_models",
    "get_async_image_models",
]


def _get_models(
    client: Client, *args: Args, **kwargs: Kwargs
) -> List[TextModel | ImageModel]:
    response = client.get("/models")
    response.raise_for_status()
    return response.json()


async def _get_async_models(
    async_client: AsyncClient, *args: Args, **kwargs: Kwargs
) -> List[TextModel | ImageModel]:
    response = await async_client.get(TEXT_API_URI)
    response.raise_for_status()
    return response.json()


def get_text_models(*args: Args, **kwargs: Kwargs) -> List[TextModel]:
    return _get_models(Client(base_url=TEXT_API_URI))


async def get_async_text_models(
    *args: Args, **kwargs: Kwargs
) -> List[TextModel]:
    return await _get_async_models(AsyncClient(base_url=TEXT_API_URI))


def get_image_models(*args: Args, **kwargs: Kwargs) -> List[ImageModel]:
    return _get_models(Client(base_url=IMAGE_API_URI))


async def get_async_image_models(
    *args: Args, **kwargs: Kwargs
) -> List[ImageModel]:
    return await _get_async_models(AsyncClient(base_url=IMAGE_API_URI))
