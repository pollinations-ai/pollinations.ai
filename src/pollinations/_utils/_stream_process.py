from ..types import StreamData, Args, Kwargs

from json import loads, JSONDecodeError

from typing import Optional

__all__: list[str] = ["_stream_process", "_feed_stream_process"]


def _stream_process(line: str, *args, **kwargs) -> Optional[str]:
    line = line.strip()
    if not line:
        return ""

    if line in ("data: [DONE]", "[DONE]"):
        return None

    chunks = []
    if "data: " in line:
        parts = line.split("data: ")
        chunks = [
            f"data: {part}" if i > 0 else part
            for i, part in enumerate(parts)
            if part.strip()
        ]
    else:
        chunks = [line]

    all_content = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        json_str = (
            chunk[len("data: ") :] if chunk.startswith("data: ") else chunk
        )

        try:
            data = loads(json_str)

            def _get(obj):
                if isinstance(obj, dict):
                    for key in ["content", "completion", "text", "response"]:
                        if (
                            key in obj
                            and isinstance(obj[key], str)
                            and obj[key]
                        ):
                            all_content.append(obj[key])
                            return

                    if "delta" in obj and isinstance(obj["delta"], dict):
                        delta = obj["delta"]
                        if (
                            "content" in delta
                            and isinstance(delta["content"], str)
                            and delta["content"]
                        ):
                            all_content.append(delta["content"])
                            return

                    for value in obj.values():
                        _get(value)

                elif isinstance(obj, list):
                    for item in obj:
                        _get(item)

            _get(data)

        except JSONDecodeError:
            if not chunk.startswith("data:") and not chunk.startswith("{"):
                all_content.append(chunk)

    return "".join(all_content)


def _feed_stream_process(
    line: StreamData, *args: Args, **kwargs: Kwargs
) -> StreamData:
    if line.startswith("data: "):
        data_str = line[len("data: ") :]
    else:
        data_str = line

    if data_str.strip() == "[DONE]":
        return None

    try:
        data = loads(data_str)
        return data
    except JSONDecodeError:
        return ""
