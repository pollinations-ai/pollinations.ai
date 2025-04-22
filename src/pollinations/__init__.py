# MIT License

# Copyright (c) 2025 pollinations

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .types import (
    PILImage,
    Prompt,
    Model,
    Seed,
    Private,
    File,
    Referrer,
    Stream,
    Filename,
    ImageData,
    Payload,
    Params,
    EmptyParams,
    StreamData,
    ErrorMessage,
    Args,
    Kwargs,
    Negative,
    Width,
    Height,
    NoLogo,
    Enhance,
    Safe,
    Save,
    System,
    Contextual,
    Messages,
    Role,
    Message,
    JsonMode,
    ReasoningEffort,
    Tools,
    ToolChoice,
    Voice,
    UseOpenAIEndpoint,
    Images,
    ImageFormat,
    Output,
    URL,
    Response,
    Request,
    Client,
    AsyncClient,
    TextModel,
    ImageModel
)
from .errors import (
    EmptyFileError,
    FailedToStreamError,
    FailedToTranscribeError,
    FileNotFoundError,
    ImproperPermissionsError,
    InvalidOrUnknownPromptError,
    NotAFileError
)
from ._core import (
    BaseClass,
    get_client,
    get_async_client,
)
from .core.text import Text
from .core.image import Image
from .helpers import get_latest
from .version import (
    __title__,
    __version__,
    __license__,
    __description__
)


__all__ = [
    "PILImage", "Prompt", "Model", "Seed", "Private", "File", "Referrer", "Stream", "Filename",
    "ImageData", "Payload", "Params", "EmptyParams", "StreamData", "ErrorMessage", "Args", "Kwargs",
    "Negative", "Width", "Height", "NoLogo", "Enhance", "Safe", "Save", "System", "Contextual",
    "Messages", "Role", "Message", "JsonMode", "ReasoningEffort", "Tools", "ToolChoice", "Voice",
    "UseOpenAIEndpoint", "Images", "ImageFormat", "Output", "URL", "Response", "Request", "Client",
    "AsyncClient", "TextModel", "ImageModel",

    "EmptyFileError", "FailedToStreamError", "FailedToTranscribeError", "FileNotFoundError",
    "ImproperPermissionsError", "InvalidOrUnknownPromptError", "NotAFileError",

    "BaseClass", "get_client", "get_async_client", 
    
    "Text", "Image",
    
    "get_latest",
    
    "__title__", "__version__", "__license__", "__description__"
]

__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "pollinations"
        except (TypeError, AttributeError):
            pass

get_latest()
