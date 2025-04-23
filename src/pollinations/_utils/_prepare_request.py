from ._encode_string import _encode_string
from ..types import Params, EmptyParams, Args, Kwargs

from random import randint

__all__: list[str] = ["_prepare_request"]


def _prepare_request(params: Params, *args: Args, **kwargs: Kwargs) -> Params | EmptyParams:
    if params is None:
        params = {}

    params["__iprompt"] = _encode_string((params.pop("__iprompt", "Error symbol alert, simple vector grapic.") + "?"))
    params["__inegative"] = _encode_string(params.pop("__inegative", "Detailed, lots of detail"))
    
    params["json"] = params.pop("json_mode", False)
    prompt = _encode_string(params.pop("__prompt", ""))
    system = _encode_string(params.pop("__system", ""))
    images = params.pop("__images", None)
    seed = params.pop("seed", None)
    

    if images or "messages" not in params or not params["messages"]:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if prompt:
            content = [{"type": "text", "text": prompt}]
            if images:
                if isinstance(images, dict):
                    content.append(images)
                else:
                    content.extend(images)
            messages.append({"role": "user", "content": content})

        params["messages"] = messages

    if seed:
        params["seed"] = (
            seed
            if isinstance(seed, (int, float))
            else randint(-2147483648, 2147483647)
        )
        
    return params
