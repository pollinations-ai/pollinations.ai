from ..types import Params, Args, Kwargs

__all__: list[str] = ["_clean_params"]


def _clean_params(params: Params, *args: Args, **kwargs: Kwargs) -> Params:
    for k in list(params.keys()):
        if k.startswith("_") or k == "openai_endpoint":
            params.pop(k)

    return params
