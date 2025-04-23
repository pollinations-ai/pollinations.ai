from .._utils._prepare_request import _prepare_request
from .._utils._stream_process import _feed_stream_process
from .._utils._clean_params import _clean_params
from ..types import (
    Client,
    AsyncClient,
    Params,
    StreamData,
    Args,
    Kwargs,
)
from ..errors import FailedToStreamError
from ._consts import (
    DEFAULT_HEADERS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)

from httpx import HTTPError, HTTPStatusError
from typing import Iterator, AsyncIterator, Optional, Callable

__all__: list[str] = [
    "_get_feed_request",
    "_get_async_feed_request",
]


def _get_feed_request(
    client: Client,
    params: Params,
    *args: Args,
    processor: Optional[Callable[[StreamData], Optional[StreamData]]] = _feed_stream_process,
    **kwargs: Kwargs
) -> Iterator[StreamData]:
    params = _prepare_request(params)
    params = _clean_params(params)
    client.headers = DEFAULT_HEADERS

    for attempt in range(DEFAULT_MAX_RETRIES + 1):
        for method in ("POST", "GET"):  
            try:
                stream_args = {
                    "method": method,
                    "url": "",
                    "timeout": DEFAULT_TIMEOUT,
                    **kwargs
                }
                if method == "POST":
                    stream_args["json"] = params

                with client.stream(**stream_args) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if not line:
                            continue
                        processed = processor(line)
                        if processed is None:
                            return
                        if processed:
                            yield processed
                return
            except HTTPStatusError as e:
                if e.response.status_code == 404 and method == "POST":
                    continue 
                if attempt == DEFAULT_MAX_RETRIES:
                    raise FailedToStreamError(FailedToStreamError.DefaultMessage)
            except HTTPError:
                if attempt == DEFAULT_MAX_RETRIES:
                    raise FailedToStreamError(FailedToStreamError.DefaultMessage)


async def _get_async_feed_request(
    client: AsyncClient,
    params: Params,
    *args: Args,
    processor: Optional[Callable[[StreamData], Optional[StreamData]]] = _feed_stream_process,
    **kwargs: Kwargs
) -> AsyncIterator[StreamData]:
    params = _prepare_request(params)
    params = _clean_params(params)
    client.headers = DEFAULT_HEADERS

    for attempt in range(DEFAULT_MAX_RETRIES + 1):
        for method in ("POST", "GET"):
            try:
                async def _generator() -> AsyncIterator[StreamData]:
                    stream_args = {
                        "method": method,
                        "url": "",
                        "timeout": DEFAULT_TIMEOUT,
                        **kwargs
                    }
                    if method == "POST":
                        stream_args["json"] = params

                    async with client.stream(**stream_args) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                            processed = processor(line)
                            if processed is None:
                                return
                            if processed:
                                yield processed
                    return

                return _generator()

            except HTTPStatusError as e:
                if e.response.status_code == 404 and method == "POST":
                    continue
                if attempt == DEFAULT_MAX_RETRIES:
                    raise FailedToStreamError(FailedToStreamError.DefaultMessage)
            except HTTPError:
                if attempt == DEFAULT_MAX_RETRIES:
                    raise FailedToStreamError(FailedToStreamError.DefaultMessage)
