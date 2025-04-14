from __future__ import annotations

import json
import httpx
import random
import base64

from pollinations._types import (
    URL,
    Client,
    AsyncClient,
    Response,
    Iterator,
    AsyncIterator,
    Optional,
    Callable,
    Any,
)
from pollinations._constants import (
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    DEFAULT_HEADERS,
)

from pollinations.utils._safe import Safe

__all__ = [
    "get_client",
    "get_async_client",
    "get_request",
    "get_async_request",
    "Stream",
]


@Safe.auto(base_url=str)
def get_client(base_url: URL) -> Client:
    return httpx.Client(
        base_url=base_url,
        headers=DEFAULT_HEADERS,
        timeout=DEFAULT_TIMEOUT,
    )


@Safe.auto(base_url=str)
def get_async_client(base_url: URL) -> AsyncClient:
    return httpx.AsyncClient(
        base_url=base_url,
        headers=DEFAULT_HEADERS,
        timeout=DEFAULT_TIMEOUT,
    )


@Safe.auto(params=(dict, {}))
def _prepare(params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    if params is None:
        return {}

    prompt = params.pop("_prompt", None)
    images = params.pop("_images", None)
    system = params.pop("_system", None)
    seed = params.pop("seed", None)

    messages = []

    if system:
        messages.append({"role": "system", "content": system})

    if prompt is not None:
        content = [{"type": "text", "text": prompt}]
        if images:
            if isinstance(images, dict):
                content.append(images)
            else:
                content.extend(images)
        messages.append({"role": "user", "content": content})

    if messages:
        params["messages"] = messages

    if seed:
        params["seed"] = _seed(seed)

    return params


@Safe.auto(value=(int, "random"))
def _seed(value: int | str) -> int:
    if isinstance(value, int):
        return value
    return random.randint(-2147483648, 2147483647)


@Safe.auto(params=(dict, {}))
def get_request(
    client: Client,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:
    params = _prepare(params)
    openai_endpoint = params.pop("openai_endpoint", False)
    response = client.post(
        "" if openai_endpoint is False else "openai", json=params, **kwargs
    )
    response.raise_for_status()

    if response.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            response = client.post(
                "" if openai_endpoint is False else "openai", json=params, **kwargs
            )
            if response.status_code == 200:
                break
    return response


@Safe.auto(params=(dict, {}))
async def get_async_request(
    client: AsyncClient,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:
    params = _prepare(params)
    openai_endpoint = params.pop("openai_endpoint", False)
    response = await client.post("", json=params, **kwargs)
    response.raise_for_status()

    if response.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            response = await client.post(
                "" if openai_endpoint is False else "openai", json=params, **kwargs
            )
            if response.status_code == 200:
                break

    return response


def get_image_request(
    client: Client,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:
    params = _prepare(params)
    params.pop("messages", None)

    prompt = params.pop("_iprompt", "Error symbol alert, simple vector grapic.") + "?"
    for k, v in params.items():
        prompt += f"{k}={v}&"
    prompt = prompt[:-1]

    response = client.get(f"prompt/{prompt}", **kwargs)
    response.raise_for_status()

    if response.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            response = client.get(f"prompt/{prompt}", **kwargs)
            if response.status_code == 200:
                break

    return response


async def get_image_async_request(
    client: AsyncClient,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:

    params = _prepare(params)
    params.pop("messages", None)

    prompt = params.pop("_iprompt", "Error symbol alert, simple vector grapic.") + "?"
    for k, v in params.items():
        prompt += f"{k}={v}&"
    prompt = prompt[:-1]

    response = await client.get(f"prompt/{prompt}", **kwargs)
    response.raise_for_status()

    if response.status_code != 200:
        for _ in range(DEFAULT_MAX_RETRIES):
            response = await client.get(f"prompt/{prompt}", **kwargs)
            if response.status_code == 200:
                break

    return response


def get_audio_request(
    client: Client,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:
    file = params.pop("file", None)

    with open(file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    payload = {
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
                            "data": encoded,
                            "format": file.split(".")[-1].lower(),
                        },
                    },
                ],
            }
        ],
        **kwargs,
    }

    request = get_request(client, payload)
    response = request.json()
    transcription = response.get("choices", [{}])[0].get("message", {}).get("content")
    return transcription


async def get_audio_async_request(
    client: AsyncClient,
    params: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> Response:
    file = params.pop("file", None)

    with open(file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    payload = {
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
                            "data": encoded,
                            "format": file.split(".")[-1].lower(),
                        },
                    },
                ],
            }
        ],
        **kwargs,
    }

    request = await get_async_request(client, payload)
    response = request.json()
    transcription = response.get("choices", [{}])[0].get("message", {}).get("content")
    return transcription


class Stream:
    @staticmethod
    @Safe.auto(line=str)
    def _process(line: str) -> Optional[str]:
        if line.startswith("data: "):
            data_str = line[len("data: ") :]
        else:
            data_str = line

        if data_str.strip() == "[DONE]":
            return None

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            return ""

        output_text = ""
        if "choices" in data and isinstance(data["choices"], list):
            for choice in data["choices"]:
                if isinstance(choice, dict):
                    delta = choice.get("delta", {})
                    content = delta.get("content", "")
                    output_text += content
        return output_text

    @staticmethod
    @Safe.auto(params=(dict, {}))
    def get_request(
        client: Client,
        params: Optional[dict[str, Any]] = None,
        processor: Optional[Callable[[str], Optional[str]]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        if processor is None:
            processor = Stream._process
        params = _prepare(params or {})
        params["stream"] = True
        openai_endpoint = params.pop("openai_endpoint", False)

        for attempt in range(DEFAULT_MAX_RETRIES + 1):
            try:
                with client.stream(
                    "POST",
                    "" if openai_endpoint is False else "openai",
                    json=params,
                    **kwargs,
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
            except httpx.HTTPError:
                if attempt == DEFAULT_MAX_RETRIES:
                    raise

    @staticmethod
    @Safe.auto(params=(dict, {}))
    async def get_async_request(
        client: AsyncClient,
        params: Optional[dict[str, Any]] = None,
        processor: Optional[Callable[[str], Optional[str]]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        if processor is None:
            processor = Stream._process
        params = _prepare(params or {})
        params["stream"] = True
        openai_endpoint = params.pop("openai_endpoint", False)

        for attempt in range(DEFAULT_MAX_RETRIES + 1):
            try:

                async def async_generator() -> AsyncIterator[str]:
                    async with client.stream(
                        "POST",
                        "" if openai_endpoint is False else "openai",
                        json=params,
                        **kwargs,
                    ) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                            processed = processor(line)
                            if processed is None:
                                continue
                            if processed:
                                yield processed

                return async_generator()
            except httpx.HTTPError:
                if attempt == DEFAULT_MAX_RETRIES:
                    raise
