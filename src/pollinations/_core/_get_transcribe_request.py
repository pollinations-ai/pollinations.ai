from .._utils.check_file import _check_file
from .._utils._prepare_request import _prepare_request
from ..types import (
    Client,
    AsyncClient,
    Params,
    Payload,
    Request,
    Response,
    Args,
    Kwargs,
)
from ..errors import FailedToTranscribeError
from ._consts import (
    DEFAULT_HEADERS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)

from base64 import b64encode

__all__: list[str] = [
    "_get_transcribe_request",
    "_get_async_transcribe_request",
]


def _get_transcribe_request(
    client: Client, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    file = params.pop("file")
    seed = params.pop("seed", 42)

    _check_file(file)

    with open(file, "rb") as f:
        data = b64encode(f.read()).decode("utf-8")        

    payload: Payload = {
        "model": "openai-audio",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe this audio. Do not wrap in quotes. Only raw text. Do not add anything else besides the transcription. Be as exact and precise as you can be.",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data,
                            "format": file.split(".")[-1].lower(),
                        },
                    },
                ],
            }
        ],
        "seed": seed,
    }

    client.headers = DEFAULT_HEADERS
    request: Request = client.post(
        "openai", json=payload, *args, **kwargs, timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = client.post(
                "openai",
                json=payload,
                *args,
                **kwargs,
                timeout=DEFAULT_TIMEOUT,
            )
            if request.status_code == 200:
                break

    response = request.json()
    try:
        transcription = (
            response.get("choices", [{}])[0].get("message", {}).get("content")
        )
    except Exception:
        raise FailedToTranscribeError(
            f"{FailedToTranscribeError.DefaultMessage[:-1]} | {file}"
        )

    return transcription


async def _get_async_transcribe_request(
    client: AsyncClient, params: Params, *args: Args, **kwargs: Kwargs
) -> Response:
    params = _prepare_request(params)
    file = params.pop("file")
    seed = params.pop("seed", 42)

    _check_file(file)


    with open(file, "rb") as f:
        data = b64encode(f.read()).decode("utf-8")    

    payload: Payload = {
        "model": "openai-audio",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Transcribe this audio. Do not wrap in quotes. Only raw text. Do not add anything else besides the transcription. Be as exact and precise as you can be.",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data,
                            "format": file.split(".")[-1].lower(),
                        },
                    },
                ],
            }
        ],
        "seed": seed,
    }

    client.headers = DEFAULT_HEADERS
    request: Request = await client.post(
        "openai", json=payload, *args, **kwargs, timeout=DEFAULT_TIMEOUT
    )
    request.raise_for_status()

    if request.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            request = await client.post(
                "openai",
                json=payload,
                *args,
                **kwargs,
                timeout=DEFAULT_TIMEOUT,
            )
            if request.status_code == 200:
                break

    response = request.json()
    try:
        transcription = (
            response.get("choices", [{}])[0].get("message", {}).get("content")
        )
    except Exception:
        raise FailedToTranscribeError(
            f"{FailedToTranscribeError.DefaultMessage[:-1]} | {file}"
        )
    return transcription
