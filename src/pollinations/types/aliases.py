from typing import Any, TypeAlias, Union, Literal, List, Dict
from io import BytesIO
from PIL.Image import Image as _Image

__all__: list[str] = [
    "PILImage",
    "Prompt",
    "Model",
    "Seed",
    "Private",
    "File",
    "Referrer",
    "Stream",
    "Filename",
    "ImageData",
    "Infinity",
    "Time",
    "Payload",
    "Params",
    "EmptyParams",
    "StreamData",
    "ErrorMessage",
    "Args",
    "Kwargs",
    "Negative",
    "Width",
    "Height",
    "NoLogo",
    "Enhance",
    "Safe",
    "Save",
    "System",
    "Contextual",
    "Messages",
    "Role",
    "Message",
    "JsonMode",
    "ReasoningEffort",
    "Tools",
    "ToolChoice",
    "Voice",
    "UseOpenAIEndpoint",
    "Images",
    "ImageFormat",
    "Output",
    "FeedType",
    "MaxData"
]

# All
Prompt: TypeAlias = str
Model: TypeAlias = str
Seed: TypeAlias = Union[int, str]
Private: TypeAlias = bool
File: TypeAlias = str
Referrer: TypeAlias = str
Stream: TypeAlias = bool
Filename: TypeAlias = str
ImageData: TypeAlias = Union[str, BytesIO]
PILImage: TypeAlias = _Image

Infinity: TypeAlias = None
Time: TypeAlias = float

Payload: TypeAlias = dict[str, Any]
Params: TypeAlias = dict[str, Any]
EmptyParams: TypeAlias = dict

StreamData: TypeAlias = str
ErrorMessage: TypeAlias = str
Args: TypeAlias = Any
Kwargs: TypeAlias = Any

# Image Specific
Negative: TypeAlias = str
Width: TypeAlias = int
Height: TypeAlias = int
NoLogo: TypeAlias = bool
Enhance: TypeAlias = bool
Safe: TypeAlias = bool
Save: TypeAlias = bool


# Text Specific
System: TypeAlias = str
Contextual: TypeAlias = bool
Messages: TypeAlias = List[Dict[str, Any]]
Role: TypeAlias = Literal["system", "user", "assistant"]
Message: TypeAlias = Dict[str, Any]
JsonMode: TypeAlias = bool
ReasoningEffort: TypeAlias = Literal["low", "medium", "high"]
Tools: TypeAlias = List[Dict[str, Any]]
ToolChoice: TypeAlias = List[str]
Voice: TypeAlias = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer", "coral", "verse", "ballad", "ash", "sage", "amuch", "dan"]
UseOpenAIEndpoint: TypeAlias = bool
Images: TypeAlias = List[Dict[str, Any]]
ImageFormat: TypeAlias = dict[str, Union[str, dict[str, str]]]
Output: TypeAlias = Union[str, Any]


# Feed
FeedType: TypeAlias = Literal["image", "text"]
MaxData: TypeAlias = int
