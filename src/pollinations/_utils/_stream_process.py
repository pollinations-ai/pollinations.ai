from ..types import StreamData, Args, Kwargs

from json import loads, JSONDecodeError

__all__: list[str] = ["_stream_process", "_feed_stream_process"]


def _stream_process(
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
    except JSONDecodeError:
        return ""

    output_text = ""
    if "choices" in data and isinstance(data["choices"], list):
        for choice in data["choices"]:
            if isinstance(choice, dict):
                delta = choice.get("delta", {})
                content = delta.get("content", "")
                output_text += content
    return output_text

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
