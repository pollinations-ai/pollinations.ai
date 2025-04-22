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

__all__: list[str] = ["_get_image_request", "_get_async_image_request"]


def _get_image_request(
    client: Client, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    prompt = params.pop("__iprompt")
    params = _clean_params(params)
    
    for k, v in params.items():
        if k == "__inegative":
            k = "negative"
        prompt += f"{k}={v}&"
    prompt = prompt[:-1]

    client.headers = DEFAULT_HEADERS
    request: Request = client.post(
        f"prompt/{prompt}", *args, **kwargs, timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = client.post(
                f"prompt/{prompt}", *args, **kwargs, timeout=DEFAULT_TIMEOUT
            )
            if request.status_code == 200:
                break
    return request


async def _get_async_image_request(
    client: AsyncClient, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    prompt = params.pop("__iprompt")
    params = _clean_params(params)
    
    for k, v in params.items():
        prompt += f"{k}={v}&"
    prompt = prompt[:-1]

    client.headers = DEFAULT_HEADERS
    request: Request = await client.post(
        f"prompt/{prompt}", *args, **kwargs, timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = await client.post(
                f"prompt/{prompt}", *args, **kwargs, timeout=DEFAULT_TIMEOUT
            )
            if request.status_code == 200:
                break
    return request
