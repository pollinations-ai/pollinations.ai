from typing import TypedDict, Optional, List

__all__: list[str] = ["TextModel", "ImageModel"]

class TextModel(TypedDict, total=False):
    name: str
    description: str
    provider: str
    input_modalities: List[str]
    output_modalities: List[str]
    vision: bool
    audio: bool
    uncensored: Optional[bool]
    reasoning: Optional[bool]
    aliases: Optional[str]
    voices: Optional[List[str]]
    
class ImageModel(TypedDict, total=False):
    name: str
