from .._utils._prepare_request import _prepare_request
from .._utils._clean_params import _clean_params
from ..types import (
    Client,
    AsyncClient,
    Params,
    Request,
    Response,
    Args,
    Kwargs,
)
from ._consts import (
    DEFAULT_HEADERS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)

__all__: list[str] = ["_get_text_request", "_get_async_text_request"]


def _get_text_request(
    client: Client, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    _use_openai = params.pop("__openai", False)
    params = _clean_params(params)
    
    client.headers = DEFAULT_HEADERS
    request: Request = client.post(
        "" if _use_openai is False else "openai",
        json=params,
        *args,
        **kwargs,
        timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = client.post(
                "" if _use_openai is False else "openai",
                json=params,
                *args,
                **kwargs,
                timeout=DEFAULT_TIMEOUT
            )
            if request.status_code == 200:
                break
    return request


async def _get_async_text_request(
    client: AsyncClient, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    _use_openai = params.pop("__openai", False)
    params = _clean_params(params)
    
    client.headers = DEFAULT_HEADERS
    request: Request = await client.post(
        "" if _use_openai is False else "openai",
        json=params,
        *args,
        **kwargs,
        timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = await client.post(
                "" if _use_openai is False else "openai",
                json=params,
                *args,
                **kwargs,
                timeout=DEFAULT_TIMEOUT
            )
            if request.status_code == 200:
                break

    return request
