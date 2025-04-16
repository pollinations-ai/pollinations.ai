from __future__ import annotations

from ..types import (
    ImageModel,
    Model,
    Private,
    Negative,
    Width,
    Height,
    NoLogo,
    Enhance,
    Safe,
    Save,
    File,
    Seed,
    Referrer,
    Prompt,
    Output,
    Request,
    Params,
    Filename,
    PILImage,
    Args,
    Kwargs,
)
from .._utils.to_pil import _to_pil
from .._utils._models import get_image_models, get_async_image_models
from .._core import (
    BaseClass,
    get_client,
    get_async_client,
    IMAGE_API_URI,
    _get_image_request,
    _get_async_image_request
)

from typing import Self, Optional, List


class Image(BaseClass):
    def __init__(
        self: Self,
        model: Optional[ImageModel] = "flux",
        width: Optional[Width] = 1024,
        height: Optional[Height] = 1024,
        seed: Optional[Seed] = "random",
        nologo: Optional[NoLogo] = False,
        private: Optional[Private] = False,
        enhance: Optional[Enhance] = False,
        safe: Optional[Safe] = False,
        referrer: Optional[Referrer] = "pollinations.py",
        *any_kwargs_will_be_passed_in_request: Args,
        **kwargs: Kwargs,
    ) -> None:
        self._client = get_client(IMAGE_API_URI)
        self._async_client = get_async_client(IMAGE_API_URI)

        self.model = model
        self.width = width
        self.height = height
        self.seed = seed
        self.nologo = nologo
        self.private = private
        self.enhance = enhance
        self.safe = safe
        self.referrer = referrer
        
        self.prompt: Prompt = None
        self.negative: Negative = None
        self.file: File = "pollinations-image.jpeg"
        
        self.image: PILImage = None
        self.response: Output = None
        self.request: Request = None

        for k, v in kwargs.items():
            setattr(self, k, v)
            
    def __call__(self: Self, prompt: Prompt, negative: Optional[Negative] = "", *args: Args, file: Optional[Filename] = "pollinations-image.jpeg", save: Save = False, **kwargs: Kwargs) -> PILImage:
        return self.Generate(prompt, negative, *args, file=file, save=save, **kwargs)
    
    def Generate(self: Self, prompt: Prompt, negative: Optional[Negative] = "", *args: Args, file: Optional[Filename] = "pollinations-image.jpeg", save: Save = False, **kwargs: Kwargs) -> PILImage:
        self.prompt = prompt
        self.negative = negative
        self.file = file
        
        params = self._setup()
        params["__iprompt"] = prompt
        params["__inegative"] = negative
        
        self.request = _get_image_request(self._client, params=params)
        self.response = self.request.content
        self.image = _to_pil(self.response)
        
        if save:
            self.image.save(self.file)
        
        return self.image
    
    async def Async(self: Self, prompt: Prompt, negative: Optional[Negative] = "", *args: Args, file: Optional[Filename] = "pollinations-image.jpeg", save: Save = False, **kwargs: Kwargs) -> PILImage:
        self.prompt = prompt
        self.negative = negative
        self.file = file
        
        params = self._setup()
        params["__iprompt"] = prompt # type: ignore
        params["__inegative"] = negative
        
        self.request = await _get_async_image_request(self._async_client, params=params)
        self.response = self.request.content
        self.image = _to_pil(self.response)
        
        if save:
            self.image.save(self.file)
        
        return self.image
    
    @staticmethod
    def Models() -> List[Model]:
        return get_image_models()
    
    @staticmethod
    async def ModelsAsync() -> List[Model]:
        return await get_async_image_models()
    
    def _setup(self: Self) -> Params:
        params: Params = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
            and k not in {"prompt", "negative", "image", "response", "request", "file"}
        }
        
        return params
