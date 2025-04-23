from ..types import Role, Prompt, Output, ImageFormat, Message, Args, Kwargs

from typing import Optional, List, Union

__all__: list[str] = ["_create_message"]


def _create_message(role: Role, prompt: Prompt | Output, images: Optional[Union[ImageFormat, List[ImageFormat]]] = None, *args: Args, **kwargs: Kwargs) -> Message:
    message = {
        "role": role,
        "content": [{"type": "text", "text": prompt}]
    }
    
    if images:
        if isinstance(images, dict):
            images = [images]
        message["content"].extend(images)
        
    return message
