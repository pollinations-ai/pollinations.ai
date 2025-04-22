from .._utils._prepare_request import _prepare_request
from .._utils._stream_process import _stream_process
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

from httpx import HTTPError
from typing import Iterator, AsyncIterator, Optional, Callable

__all__: list[str] = [
    "_get_stream_text_request",
    "_get_async_stream_text_request",
]


def _get_stream_text_request(
    client: Client,
    params: Params,
    *args: Args,
    processor: Optional[
        Callable[[StreamData], Optional[StreamData]]
    ] = _stream_process,
    **kwargs: Kwargs
) -> Iterator[StreamData]:
    params = _prepare_request(params)
    params["stream"] = True
    _use_openai = params.pop("__openai", False)
    params = _clean_params(params)

    client.headers = DEFAULT_HEADERS

    for attempt in range(DEFAULT_MAX_RETRIES + 1):
        try:
            with client.stream(
                "POST",
                "" if _use_openai is False else "openai",
                json=params,
                *args,
                **kwargs,
                timeout=DEFAULT_TIMEOUT
            ) as response:
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
        except HTTPError:
            if attempt == DEFAULT_MAX_RETRIES:
                raise FailedToStreamError(FailedToStreamError.DefaultMessage)


async def _get_async_stream_text_request(
    client: AsyncClient,
    params: Params,
    *args: Args,
    processor: Optional[
        Callable[[StreamData], Optional[StreamData]]
    ] = _stream_process,
    **kwargs: Kwargs
) -> AsyncIterator[StreamData]:
    params = _prepare_request(params)
    params["stream"] = True
    _use_openai = params.pop("__openai", False)
    params = _clean_params(params)

    client.headers = DEFAULT_HEADERS

    for attempt in range(DEFAULT_MAX_RETRIES + 1):
        try:

            async def _generator() -> AsyncIterator[StreamData]:
                async with client.stream(
                    "POST",
                    "" if _use_openai is False else "openai",
                    json=params,
                    *args,
                    **kwargs,
                    timeout=DEFAULT_TIMEOUT
                ) as response:
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

        except HTTPError:
            if attempt == DEFAULT_MAX_RETRIES:
                raise FailedToStreamError(FailedToStreamError.DefaultMessage)
