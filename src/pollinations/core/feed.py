from __future__ import annotations

from ..types import (
    StreamData,
    FeedType,
    MaxData,
    Infinity,
    Time,
    Args,
    Kwargs,
)

from .._core import (
    BaseClass,
    get_client,
    get_async_client,
    TEXT_API_URI,
    IMAGE_API_URI,
    _get_feed_request,
    _get_async_feed_request,
)

from typing import Self, Optional, List, Iterator, AsyncIterator
from time import time as now

__all__: list[str] = ["Feed"]


class Feed(BaseClass):
    def __init__(
        self: Self,
        type: FeedType = "image",
        max_data: Optional[MaxData | Infinity] = None,
        *args: Args,
        **kwargs: Kwargs,
    ) -> None:
        self._text_client = get_client(TEXT_API_URI + "feed")
        self._image_client = get_client(IMAGE_API_URI + "feed")
        self._async_text_client = get_async_client(TEXT_API_URI + "feed")
        self._async_image_client = get_async_client(IMAGE_API_URI + "feed")

        self.type = type
        self.data: List[StreamData] = []
        self.max_data = max_data

    def __call__(
        self: Self, *args: Args, **kwargs: Kwargs
    ) -> Iterator[Feed.Data]:
        return self.Get(*args, **kwargs)

    def Get(self: Self, *args: Args, **kwargs: Kwargs) -> Iterator[Feed.Data]:
        self.data.clear()
        counter = 0

        client = (
            self._image_client if self.type == "image" else self._text_client
        )
        for item in _get_feed_request(client, kwargs, *args, **kwargs):
            wrapped = self.Data(data=item, time=now())
            self.data.append(wrapped)
            yield wrapped
            counter += 1
            if self.max_data and counter >= self.max_data:
                break

    async def Async(
        self: Self, *args: Args, **kwargs: Kwargs
    ) -> AsyncIterator[Feed.Data]:
        self.data.clear()
        counter = 0

        client = (
            self._async_image_client
            if self.type == "image"
            else self._async_text_client
        )
        async for item in await _get_async_feed_request(
            client, kwargs, *args, **kwargs
        ):
            wrapped = self.Data(data=item, time=now())
            self.data.append(wrapped)
            yield wrapped
            counter += 1
            if self.max_data and counter >= self.max_data:
                break

    class Data(BaseClass):
        def __init__(
            self: Self,
            data: StreamData,
            time: Time,
            *args: Args,
            **kwargs: Kwargs,
        ) -> None:
            self.data = data
            self.time = time

        def __call__(self: Self, *args: Args, **kwargs: Kwargs) -> StreamData:
            return self.data
