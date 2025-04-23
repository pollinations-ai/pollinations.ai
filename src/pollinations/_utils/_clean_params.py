from ..types import Params, Args, Kwargs

__all__: list[str] = ["_clean_params"]


def _clean_params(params: Params, *args: Args, **kwargs: Kwargs) -> Params:
    for k in list(params.keys()):
        if k.startswith("_") or k == "openai_endpoint" or k == "status":
            params.pop(k)
            
    if "tools" in params and "tool_choices" in params:
        if params["tools"] == []:
            params.pop("tools")
        if params["tool_choices"] == []:
            params.pop("tool_choices")
            
    return params
