from __future__ import annotations

from pollinations._types import Image as _P_Image
from pollinations._types import List, Union, Dict, Any, Optional
from pollinations._constants import IMAGE_API_URI
from pollinations.utils._request import (
    get_client,
    get_async_client,
    get_image_request,
    get_image_async_request,
)
from pollinations.utils._safe import Safe
from pollinations.utils._models import image_models
from pollinations.utils._image import (
    _safe_check,
    _read_image_content,
    _read_image_content_async,
    _to_pil,
)

__all__ = ["Image"]


class Image:
    __all__ = [
        "__init__",
        "__call__",
        "__repr__",
        "__str__",
        "models",
        "Async",
    ]

    @Safe.auto(
        model=str,
        seed=(int, "random"),
        width=int,
        height=int,
        nologo=bool,
        private=bool,
        enhance=bool,
        safe=bool,
        referrer=str,
    )
    def __init__(
        self,
        model: str = "flux",
        seed: Union[int, str] = "random",
        file: str = "pollinations-image.png",
        width: int = 1024,
        height: int = 1024,
        nologo: bool = False,
        private: bool = False,
        enhance: bool = False,
        negative: str = None,
        safe: bool = False,
        referrer: str = "pollinations.py",
        *any_kwargs_will_be_passed_in_request,
        **kwargs,
    ) -> None:
        self._client = get_client(IMAGE_API_URI)
        self._async_client = get_async_client(IMAGE_API_URI)

        self.model = model
        self.seed = seed
        self.file = file
        self.width = width
        self.height = height
        self.nologo = nologo
        self.private = private
        self.enhance = enhance
        self.negative = negative
        self.safe = safe
        self.referrer = referrer

        self.prompt: Optional[str] = None
        self.image: Optional[_P_Image.Image] = None
        self.response: Optional[str] = None
        self.request: Optional[bytes] = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    @Safe.auto(prompt=str, save=(bool, False))
    def __call__(self, prompt: str, save: bool = False) -> _P_Image.Image:
        self.prompt = prompt
        params = self._setup()
        params["_iprompt"] = prompt
        self.request = get_image_request(self._client, params=params)
        self.response = _read_image_content(self.request.content)
        self.image = _to_pil(self.response)
        if save:
            _safe_check(self.file)
            self.image.save(self.file)

        return self.image

    @Safe.auto(prompt=str, save=(bool, False))
    async def Async(self, prompt: str, save: bool = False) -> _P_Image.Image:
        self.prompt = prompt
        params = self._setup()
        params["_iprompt"] = prompt
        self.request = await get_image_async_request(self._async_client, params=params)
        self.response = await _read_image_content_async(self.request.content)
        self.image = _to_pil(self.response)
        if save:
            _safe_check(self.file)
            self.image.save(self.file)

        return self.image

    def _setup(self) -> Dict[str, Any]:
        params = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
            and k not in {"prompt", "image", "response", "request", "file"}
        }

        return params

    @staticmethod
    def models() -> List:
        return image_models()

    def __repr__(self) -> str:
        def _short(value):
            if isinstance(value, (str, bytes)) and len(value) > 50:
                return f"{value[:50]}... [{len(value) - 50} more]"
            return repr(value)

        items = []

        for k, v in self.__dict__.items():
            if k in {"_client", "_async_client"}:
                continue
            items.append(f"{k}={_short(v)}")

        return f"{self.__class__.__name__}({', '.join(items)})"

    __str__ = __repr__
