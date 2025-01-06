"""
```
pollinations.ai: (https://pollinations.ai/) 

Work with the best generative models from Pollinations using this Python SDK.
```

## Installing
```shell
pip install -U pollinations
pip install -U pollinations.ai

# Linux/macOS
python3 -m pip install -U pollinations
python3 -m pip install -U pollinations.ai

# Windows
py -3 -m pip install -U pollinations
py -3 -m pip install -U pollinations.ai
```

## Image Generation
```python
import pollinations

image_model = pollinations.Image(
    model=pollinations.Image.flux(),
    seed="random",
    width=1024,
    height=1024,
    enhance=False,
    nologo=True,
    private=True,
    safe=False
)  # or pollinations.Image() to use defaults

image = image_model(
    prompt="A cat with flowers around it."
)

print(image.prompt, image.response)

image.save(
    file="pollinations-image.png"
)

print(pollinations.Image.models())
print(pollinations.Image.flux())
print(pollinations.Image.flux.info())
```
### Async Image Generation
```python
image_model = pollinations.Async.Image()  # Has ALL features and functionality of normal Image class

image = await image_model(
    prompt="A cat with flowers around it."
)
```
## Text Generation
```python
import pollinations

text_model = pollinations.Text(
    model=pollinations.Text.openai(),
    system="You are a helpful assistant.",
    contextual=True,
    messages=[  # or [] or None
        pollinations.Text.Message(
            role="user",
            content="What is the capital of France?"
        ),
        pollinations.Text.Message(
            role="assistant",
            content="The capital of France is Paris."
        )
    ],
    seed="random",
    jsonMode=False
)

response = text_model(
    prompt="Hello.",
    display=True,  # Simulate typing,
    encode=True  # Use proper encoding
)

print(response.prompt, response.response)

print(pollinations.Text.models())
print(pollinations.Text.openai())
print(pollinations.Text.openai.info())
```
### Async Text Generation
```python
text_model = pollinations.Async.Text()  # Has ALL features and functionality of normal Text class

response = await text_model(
    prompt="Hello."
)
```
## Image Request Building
```python
import pollinations

image_request = pollinations.Image.Request(
    model=pollinations.Image.flux(),
    prompt="A cat with flowers around it.",
    seed="random",
    width=1024,
    height=1024,
    enhance=False,
    nologo=True,
    private=True,
    safe=False
)

image = image_request()

print(image.model, image.prompt, image.response)
```

## Text Request Building
```python
import pollinations

text_request = pollinations.Text.Request(
    model=pollinations.Text.openai(),
    prompt="Hello, how are you?",
    system="You are a helpful assistant.",
    contextual=True,
    messages=[  # or [] or None
        pollinations.Text.Message(
            role="user",
            content="What is the capital of France?"
        ),
        pollinations.Text.Message(
            role="assistant",
            content="The capital of France is Paris."
        )
    ],
    images=[
        pollinations.Text.Message.image("my_file.png"),
        pollinations.Text.Message.image("my_file2.png")
    ],
    seed="random",
    jsonMode=False
)

response = text_request(
    encode=True  # Use proper encoding
)
print(response)
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Repository](https://github.com/pollinations-ai/pollinations.ai)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)

"""

__version__ = "2.3.6"

import requests
import datetime
import chardet
import aiohttp
import asyncio
import typing
import random
import string
import base64
import json
import time
import enum
import sys
import os


class API(enum.Enum):
    """
    Enumeration representing API configuration details.

    Attributes:
        TEXT (str): Endpoint for text-based APIs.
        IMAGE (str): Endpoint for image-based APIs.
        HEADERS (dict): HTTP headers required for API requests.
        TIMEOUT (int): Default timeout for API requests in seconds.
    """

    TEXT = "text.pollinations.ai"
    IMAGE = "image.pollinations.ai"
    HEADERS = {"Content-Type": "application/json"}
    TIMEOUT = 60


class Model(object):
    """
    Represents a model's configuration & details.

    Attributes:
        name (str): The name of the model.
        type (str): The type/category of the model (e.g., chat, image).
        censored (bool): Whether the model is subject to content censorship.
        description (str): A brief description of the model.
        baseModel (bool): Indicates if the model is a base model.

    Methods:
        info(*args, **kwargs): Returns a dictionary representation of the model's attributes.
        __call__(*args, **kwargs): Returns the name of the model.
        __str__(*args, **kwargs): Returns the name of the model as a string.
        __repr__(*args, **kwargs): Returns a JSON-formatted string of the model attributes.
    """

    def __init__(
        self,
        name: str = None,
        type: str = None,
        censored: bool = False,
        description: str = None,
        baseModel: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.name = name
        self.type = type
        self.censored = censored
        self.description = description
        self.baseModel = baseModel

    def info(self, *args, **kwargs) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "censored": self.censored,
            "description": self.description,
            "baseModel": self.baseModel,
        }

    def __call__(self, *args, **kwargs):
        return self.name

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.info(), indent=4)


class Text(object):
    """
    Manages interactions with text-based AI models.

    Attributes:
        model (str): The model's name.
        system (str): Systeml prompt or configuration.
        contextual (bool): Indicates if the interaction is context-aware.
        messages (list): List of conversation messages.
        seed (int or str): Seed for model behavior.
        jsonMode (bool): Whether the response should be in JSON format.

    Methods:
        image(file: str | list, *args, **kwargs): Vision capability of the model. (openai model only)
        __call__(prompt: str, display: bool, *args, encode: bool, **kwargs): Sends a prompt to the model and processes the response.
        __str__(): Returns a string representation of the Text instance.
        __repr__(): Returns a JSON-formatted string of the Text instance attributes.
        models(*args, **kwargs): Fetches a tuple of available model names.
    """

    def __init__(
        self,
        model: str = "openai",
        system: str = "",
        contextual: bool = False,
        messages: list = [],
        seed: int = "random",
        jsonMode: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.timestamp = datetime.datetime.now()
        self.model = model
        self.system = system
        self.contextual = contextual
        self.messages = messages
        self.seed = seed
        self.jsonMode = jsonMode

        if self.system is not None and self.system != "":
            self.messages = [Text.Message("system", self.system)] + self.messages

        self.images = None

        self.prompt = None
        self.request = None
        self.time = None

    def image(self, file: str | list, *args, **kwargs):
        # broken, get this whenever using image(s): An error occurred: 500 - Request failed with status code 400
        if isinstance(file, str):
            self.images = Text.Message.image(file)
        else:
            self.images = [Text.Message.image(f) for f in file]

        return self

    def __call__(
        self,
        prompt: str = None,
        display: bool = False,
        *args,
        encode: bool = False,
        **kwargs,
    ):
        if prompt is None:
            if len(self.messages) > 0:
                self.prompt = self.messages[-1].content
        else:
            self.prompt = prompt

        self.messages = [
            Text.Message(message.get("role", "user"), message.get("content", ""))
            if isinstance(message, dict)
            else message
            for message in self.messages
        ]

        request = Text.Request(
            model=self.model,
            prompt=self.prompt,
            system=self.system,
            contextual=self.contextual,
            messages=self.messages,
            images=self.images,
            seed=self.seed,
            jsonMode=self.jsonMode,
        )

        self.request = request
        self.response = request(encode=encode)
        self.time = datetime.datetime.now()

        self.messages.append(Text.Message("user", self.prompt))
        self.messages.append(Text.Message("assistant", self.response))

        if display is True:
            for i, char in enumerate(self.response):
                delay = (
                    (0.1, 0.3)
                    if i > 0
                    and self.response[i - 1]
                    not in set(string.ascii_letters + string.digits + " \t\n")
                    else (0.01, 0.05)
                )

                time.sleep(random.uniform(*delay))
                sys.stdout.write(char)
                sys.stdout.flush()
            print()

        return self

    def __str__(self):
        return f"{self.__class__.__name__}(model={self.model}, prompt={self.prompt}, system={self.system}, contextual={self.contextual}, messages={len(self.messages)}, timestamp={self.timestamp})"

    def __repr__(self):
        return json.dumps(
            {
                "class": self.__class__.__name__,
                "model": self.model,
                "prompt": self.prompt,
                "system": self.system,
                "contextual": self.contextual,
                "messages": len(self.messages),
                "timestamp": str(self.timestamp),
            },
            indent=4,
        )

    @staticmethod
    def models(*args, **kwargs) -> tuple:
        response = requests.get(
            url=f"https://{API.TEXT.value}/models",
            headers=API.HEADERS.value,
            timeout=API.TIMEOUT.value,
        )
        if response.status_code == 200:
            return tuple(model["name"] for model in response.json())
        return tuple()

    class Message(object):
        """
        Represents a single message in a conversation with a model.

        Attributes:
            role (str): The role of the sender (user, assistant, system).
            content (str): The textual content of the message.
            images (dict | list): Optional image content associated with the message.
            timestamp (datetime): The creation timestamp of the message.

        Methods:
            image(file: str, *args, **kwargs): Converts an image file to a dictionary for inclusion in a message.
            __call__(*args, **kwargs): Converts the message object into a dictionary format.
            __str__(*args, **kwargs): Returns a string representation of the message.
            __repr__(*args, **kwargs): Returns a JSON-formatted string of the message attributes.
        """

        class Role(object):
            USER = "user"
            ASSISTANT = "assistant"
            SYSTEM = "system"

        def __init__(self, role: str, content: str, images: dict | list = None):
            self.timestamp = datetime.datetime.now()
            self.role = str(role) if role in ["user", "assistant", "system"] else "user"
            self.content = str(content)
            self.images = images
            if self.images is not None:
                self.images = [images] if isinstance(images, dict) else list(images)

        @staticmethod
        def image(file: str, *args, **kwargs) -> dict:
            if not os.path.exists(file):
                return None

            with open(file, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
                file_extension = file.split(".")[-1].lower()

            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "gif": "image/gif",
                "webp": "image/webp",
            }
            mime_type = mime_types.get(file_extension, "image/png")

            return {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"},
            }

        def __call__(self, *args, **kwargs):
            message = {
                "role": self.role,
            }
            message["content"] = [{"type": "text", "text": self.content}]
            if self.images is not None:
                if isinstance(self.images, dict):
                    self.images = [self.images]
                message["content"].extend(self.images)

            return message

        def __str__(self, *args, **kwargs):
            return f"{self.__class__.__name__}(role={self.role}, content={self.content}, images={len(self.images)}, timestamp={self.timestamp})"

        def __repr__(self, *args, **kwargs):
            return json.dumps(
                {
                    "class": self.__class__.__name__,
                    "role": self.role,
                    "content": self.content,
                    "images": len(self.images) if self.images is not None else 0,
                    "timestamp": str(self.timestamp),
                },
                indent=4,
            )

    class Request(object):
        """
        Handles requests to text-based AI APIs.

        Attributes:
            model (str): The name of the model.
            prompt (str): The input text prompt.
            system (str): System configuration for the request.
            contextual (bool): Whether the request maintains contextual awareness.
            messages (list): List of conversation messages.
            images (list): Optional list of image for vision (openai model only).
            seed (int or str): Random seed for the request.
            jsonMode (bool): Whether the response should be in JSON format.

        Methods:
            __call__(encode: bool, *args, **kwargs): Sends the API request and processes the response.
            __str__(*args, **kwargs): Returns a string representation of the request instance.
            __repr__(*args, **kwargs): Returns a JSON-formatted string of the request attributes.
        """

        def __init__(
            self,
            model: str,
            prompt: str,
            *args,
            system: str = "",
            contextual: bool = False,
            messages: typing.List[dict] = None,
            images: typing.List[dict] = None,
            seed: typing.Union[str, int] = "random",
            jsonMode: bool = False,
            **kwargs,
        ) -> None:
            self.timestamp = datetime.datetime.now()
            self.model = str(model) if model in Text.models() else "openai"
            self.prompt = str(prompt)
            self.system = str(system)
            self.contextual = contextual if isinstance(contextual, bool) else False
            self.messages = messages or []
            self.images = images
            self.seed = random.randint(0, 9999999999) if seed == "random" else int(seed)
            self.jsonMode = jsonMode if isinstance(jsonMode, bool) else False

        def __call__(self, encode: bool = False, *args, **kwargs):
            try:
                if self.contextual:
                    messages = [
                        message() if isinstance(message, Text.Message) else message
                        for message in self.messages
                    ]

                    if self.system and (
                        not messages or messages[0]["role"] != "system"
                    ):
                        system_message = Text.Message("system", self.system)()
                        messages.insert(0, system_message)

                    if self.prompt is not None:
                        if self.images is not None and len(self.images) > 0:
                            messages.append(
                                Text.Message("user", self.prompt, self.images)()
                            )
                        else:
                            messages.append(Text.Message("user", self.prompt)())

                    request = requests.post(
                        f"https://{API.TEXT.value}/",
                        json={
                            "model": self.model,
                            "messages": messages,
                            "seed": self.seed,
                            "jsonMode": self.jsonMode,
                        },
                        headers=API.HEADERS.value,
                        timeout=API.TIMEOUT.value,
                    )
                else:
                    params = {
                        "model": self.model,
                        "seed": self.seed,
                        "json": self.jsonMode,
                    }
                    if self.system:
                        params["system"] = self.system

                    request = requests.get(
                        f"https://{API.TEXT.value}/{self.prompt}",
                        params=params,
                        headers=API.HEADERS.value,
                        timeout=API.TIMEOUT.value,
                    )

                if request.status_code == 200:
                    if self.jsonMode:
                        try:
                            response = request.json()
                        except Exception:
                            response = request.text
                    else:
                        response = request.text

                    if encode:
                        try:
                            response = response.encode("utf-8")
                            response = response.decode("utf-8")
                        except Exception:
                            try:
                                detection = chardet.detect(request.content)
                                response = response.decode(detection["encoding"])
                            except Exception:
                                pass

                    return response
                else:
                    return f"An error occurred: {request.status_code} - {request.text}"

            except Exception as e:
                return f"An error occurred: {e}"

        def __str__(self, *args, **kwargs):
            return f"{self.__class__.__name__}(model={self.model}, prompt={self.prompt}, system={self.system}, contextual={self.contextual}, messages={len(self.messages)}, timestamp={self.timestamp})"

        def __repr__(self, *args, **kwargs):
            return json.dumps(
                {
                    "class": self.__class__.__name__,
                    "model": self.model,
                    "prompt": self.prompt,
                    "system": self.system,
                    "contextual": self.contextual,
                    "messages": len(self.messages),
                    "images": len(self.images) if self.images is not None else 0,
                    "timestamp": str(self.timestamp),
                },
                indent=4,
            )

    openai = Model(
        name="openai",
        type="chat",
        censored=True,
        description="OpenAI GPT-4o",
        baseModel=True,
    )

    qwen = Model(
        name="qwen",
        type="chat",
        censored=False,
        description="Qwen 2.5 72B",
        baseModel=True,
    )

    qwen_coder = Model(
        name="qwen-coder",
        type="chat",
        censored=False,
        description="Qwen 2.5 Coder 32B",
        baseModel=True,
    )

    llama = Model(
        name="llama",
        type="chat",
        censored=False,
        description="Llama 3.3 70B",
        baseModel=True,
    )

    mistral = Model(
        name="mistral",
        type="chat",
        censored=False,
        description="Mistral Nemo",
        baseModel=True,
    )

    mistral_large = Model(
        name="mistral-large",
        type="chat",
        censored=False,
        description="Mistral Large (v2)",
        baseModel=True,
    )

    command_r = Model(
        name="command-r",
        type="chat",
        censored=False,
        description="Command-R",
        baseModel=False,
    )

    unity = Model(
        name="unity",
        type="chat",
        censored=False,
        description="Unity with Mistral Large by Unity AI Lab",
        baseModel=False,
    )

    midjourney = Model(
        name="midjourney",
        type="chat",
        censored=True,
        description="Midijourney musical transformer",
        baseModel=False,
    )

    rtist = Model(
        name="rtist",
        type="chat",
        censored=True,
        description="Rtist image generator by @bqrio",
        baseModel=False,
    )

    searchgpt = Model(
        name="searchgpt",
        type="chat",
        censored=True,
        description="SearchGPT with realtime news and web search",
        baseModel=False,
    )

    evil = Model(
        name="evil",
        type="chat",
        censored=False,
        description="Evil Mode - Experimental",
        baseModel=False,
    )

    p1 = Model(
        name="p1",
        type="chat",
        censored=False,
        description="Pollinations 1 (OptiLLM)",
        baseModel=False,
    )
    
    deepseek = Model(
            name="deepseek",
            type="chat",
            censored=True,
            description="DeepSeek-V3",
            baseModel=True
        )


class Image(object):
    """
    Manages interactions with image-based AI models.

    Attributes:
        model (str): The model's name.
        seed (int or str): Seed for model behavior.
        width (int): The width of the output image.
        height (int): The height of the output image.
        enhance (bool): Whether the prompt should be AI enhanced.
        nologo (bool): Removes logos from output images if True.
        private (bool): Indicates if the request is private from feed.
        safe (bool): Ensures safe content generation (strict NSFW filtering).

    Methods:
        __call__(prompt: str, *args): Sends a prompt to the model and processes the response.
        save(file: str): Saves the response image to a file.
        __str__(*args, **kwargs): Returns a string representation of the Image instance.
        __repr__(*args, **kwargs): Returns a dictionary representation of the Image instance attributes.
    """

    def __init__(
        self,
        model: str = "flux",
        seed: typing.Union[str, int] = "random",
        width: int = 1024,
        height: int = 1024,
        enhance: bool = False,
        nologo: bool = False,
        private: bool = False,
        safe: bool = False,
    ):
        self.timestamp = datetime.datetime.now()
        self.model = str(model) if model in Image.models() else "flux"
        self.seed = seed
        self.width = width if isinstance(width, int) else 1024
        self.height = height if isinstance(height, int) else 1024
        self.enhance = enhance if isinstance(enhance, bool) else False
        self.nologo = nologo if isinstance(nologo, bool) else False
        self.private = private if isinstance(private, bool) else False
        self.safe = safe if isinstance(safe, bool) else False

        self.prompt = None
        self.response = None
        self.file = "pollinations-image.png"

    def __call__(self, prompt: str, *args):
        seed = (
            random.randint(0, 9999999999) if self.seed == "random" else int(self.seed)
        )

        request = Image.Request(
            model=self.model,
            prompt=prompt,
            seed=seed,
            width=self.width,
            height=self.height,
            enhance=self.enhance,
            nologo=self.nologo,
            private=self.private,
            safe=self.safe,
        )

        self.prompt = prompt
        self.response = request()

        return self

    def save(self, file: str = "pollinations-image.png"):
        self.file = file

        with open(file, "wb") as f:
            for chunk in self.response.response.iter_content(chunk_size=8192):
                f.write(chunk)

        return self

    def __str__(self, *args, **kwargs):
        return f"{self.__class__.__name__}(model={self.model}, seed={self.seed}, width={self.width}, height={self.height}, enhance={self.enhance}, nologo={self.nologo}, private={self.private}, safe={self.safe})"

    def __repr__(self, *args, **kwargs):
        return {
            "model": self.model,
            "seed": self.seed,
            "width": self.width,
            "height": self.height,
            "enhance": self.enhance,
            "nologo": self.nologo,
            "private": self.private,
            "safe": self.safe,
            "timestamp": str(self.timestamp),
        }

    class Request(object):
        """
        Handles requests to image-based AI APIs.

        Attributes:
            model (str): The name of the model.
            prompt (str): The input description or prompt for image generation.
            seed (int or str): Seed for ensuring consistent outputs.
            width (int): The desired width of the output image.
            height (int): The desired height of the output image.
            enhance (bool): Whether the prompt should be AI enhanced.
            nologo (bool): Removes logos from output images if True.
            private (bool): Indicates if the request is private from feed.
            safe (bool): Ensures safe content generation (strict NSFW filtering).
            file (str): The file path for saving the generated image.

        Methods:
            __call__(*args, encode: bool, **kwargs): Sends the image generation request to the API and processes the response.
            save(file: str): Saves the response image to the specified file.
            __str__(*args, **kwargs): Returns a string representation of the request instance.
            __repr__(*args, **kwargs): Returns a JSON-formatted string of the request attributes.
        """

        def __init__(
            self,
            model: str = "flux",
            prompt: str = "",
            seed: typing.Union[str, int] = "random",
            width: int = 1024,
            height: int = 1024,
            enhance: bool = False,
            nologo: bool = False,
            private: bool = False,
            safe: bool = False,
        ):
            self.timestamp = datetime.datetime.now()
            self.model = str(model) if model in Image.models() else "flux"
            self.prompt = str(prompt)
            self.seed = random.randint(1, 999999999) if seed == "random" else seed
            self.width = width if isinstance(width, int) else 1024
            self.height = height if isinstance(height, int) else 1024
            self.enhance = enhance if isinstance(enhance, bool) else False
            self.nologo = nologo if isinstance(nologo, bool) else False
            self.private = private if isinstance(private, bool) else False
            self.safe = safe if isinstance(safe, bool) else False

            self.response = None
            self.time = None
            self.params = None

        def __call__(self, *args, **kwargs):
            try:
                params = {
                    "safe": self.safe,
                    "seed": self.seed,
                    "width": self.width,
                    "height": self.height,
                    "nologo": self.nologo,
                    "private": self.private,
                    "model": self.model,
                    "enhance": self.enhance,
                }

                query_params = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"https://{API.IMAGE.value}/prompt/{self.prompt}?{query_params}"

                response = requests.get(
                    url=url, headers=API.HEADERS.value, timeout=API.TIMEOUT.value
                )

                self.response = response
                self.time = datetime.datetime.now()
                self.params = params

                return self

            except Exception:
                return self

        def __str__(self, *args, **kwargs):
            return f"{self.__class__.__name__}(model={self.model}, seed={self.seed}, width={self.width}, height={self.height}, enhance={self.enhance}, nologo={self.nologo}, private={self.private}, safe={self.safe})"

        def __repr__(self, *args, **kwargs):
            return {
                "model": self.model,
                "seed": self.seed,
                "width": self.width,
                "height": self.height,
                "enhance": self.enhance,
                "nologo": self.nologo,
                "private": self.private,
                "safe": self.safe,
                "timestamp": str(self.timestamp),
            }

    @staticmethod
    def models(*args, **kwargs) -> tuple:
        response = requests.get(
            url=f"https://{API.IMAGE.value}/models",
            headers=API.HEADERS.value,
            timeout=API.TIMEOUT.value,
        )
        if response.status_code == 200:
            return tuple(response.json())
        return tuple()

    flux = Model(
        name="flux",
        type="image",
        censored=False,
        description="Flux Image Generative Model",
        baseModel=True,
    )

    flux_realism = Model(
        name="flux-realism",
        type="image",
        censored=False,
        description="Flux Realism Image Generative Model",
        baseModel=False,
    )

    flux_cablyai = Model(
        name="flux-cablyai",
        type="image",
        censored=False,
        description="Flux 1.1 Image Generative Model",
        baseModel=False,
    )

    flux_anime = Model(
        name="flux-anime",
        type="image",
        censored=False,
        description="Flux Anime Image Generative Model",
        baseModel=False,
    )

    flux_3d = Model(
        name="flux-3d",
        type="image",
        censored=False,
        description="Flux 3D Image Generative Model",
        baseModel=False,
    )

    flux_pro = Model(
        name="flux-pro",
        type="image",
        censored=False,
        description="Flux Pro Image Generative Model",
        baseModel=False,
    )

    any_dark = Model(
        name="any-dark",
        type="image",
        censored=False,
        description="Any Dark Image Generative Model",
        baseModel=False,
    )

    turbo = Model(
        name="turbo",
        type="image",
        censored=False,
        description="Turbo Image Generative Model",
        baseModel=True,
    )


class Async:
    """
    Contains the async versions of Text and Image classes.
    """

    class Text:
        """
        ASYNC VERSION

        Manages interactions with text-based AI models.

        Attributes:
            model (str): The model's name.
            system (str): Systeml prompt or configuration.
            contextual (bool): Indicates if the interaction is context-aware.
            messages (list): List of conversation messages.
            seed (int or str): Seed for model behavior.
            jsonMode (bool): Whether the response should be in JSON format.

        Methods:
            image(file: str | list, *args, **kwargs): Vision capability of the model. (openai model only)
            __call__(prompt: str, display: bool, *args, encode: bool, **kwargs): Sends a prompt to the model and processes the response.
            __str__(): Returns a string representation of the Text instance.
            __repr__(): Returns a JSON-formatted string of the Text instance attributes.
            models(*args, **kwargs): Fetches a tuple of available model names.
        """

        def __init__(
            self,
            model: str = "openai",
            system: str = "",
            contextual: bool = False,
            messages: list = [],
            seed: int = "random",
            jsonMode: bool = False,
            *args,
            **kwargs,
        ) -> None:
            self.timestamp = datetime.datetime.now()
            self.model = model
            self.system = system
            self.contextual = contextual
            self.messages = messages
            self.seed = seed
            self.jsonMode = jsonMode

            if self.system is not None and self.system != "":
                self.messages = [
                    Async.Text.Message("system", self.system)
                ] + self.messages

            self.images = None
            self.prompt = None
            self.request = None
            self.time = None

        async def image(self, file: str | list, *args, **kwargs):
            if isinstance(file, str):
                self.images = await Async.Text.Message.image(file)
            else:
                self.images = [await Async.Text.Message.image(f) for f in file]
            return self

        async def __call__(
            self,
            prompt: str = None,
            display: bool = False,
            *args,
            encode: bool = False,
            **kwargs,
        ):
            if prompt is None:
                if len(self.messages) > 0:
                    self.prompt = self.messages[-1].content
            else:
                self.prompt = prompt

            self.messages = [
                Async.Text.Message(
                    message.get("role", "user"), message.get("content", "")
                )
                if isinstance(message, dict)
                else message
                for message in self.messages
            ]

            request = Async.Text.Request(
                model=self.model,
                prompt=self.prompt,
                system=self.system,
                contextual=self.contextual,
                messages=self.messages,
                images=self.images,
                seed=self.seed,
                jsonMode=self.jsonMode,
            )

            self.request = request
            self.response = await request(encode=encode)
            self.time = datetime.datetime.now()

            self.messages.append(Async.Text.Message("user", self.prompt))
            self.messages.append(Async.Text.Message("assistant", self.response))

            if display is True:
                for i, char in enumerate(self.response):
                    delay = (
                        (0.1, 0.3)
                        if i > 0
                        and self.response[i - 1]
                        not in set(string.ascii_letters + string.digits + " \t\n")
                        else (0.01, 0.05)
                    )

                    await asyncio.sleep(random.uniform(*delay))
                    sys.stdout.write(char)
                    sys.stdout.flush()
                print()

            return self

        @staticmethod
        async def models(*args, **kwargs) -> tuple:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"https://{API.TEXT.value}/models",
                    headers=API.HEADERS.value,
                    timeout=aiohttp.ClientTimeout(total=API.TIMEOUT.value),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return tuple(model["name"] for model in data)
                    return tuple()

        def __str__(self):
            return f"{self.__class__.__name__}(model={self.model}, prompt={self.prompt}, system={self.system}, contextual={self.contextual}, messages={len(self.messages)}, timestamp={self.timestamp})"

        def __repr__(self):
            return json.dumps(
                {
                    "class": self.__class__.__name__,
                    "model": self.model,
                    "prompt": self.prompt,
                    "system": self.system,
                    "contextual": self.contextual,
                    "messages": len(self.messages),
                    "timestamp": str(self.timestamp),
                },
                indent=4,
            )

        class Message:
            """
            ASYNC VERSION

            Represents a single message in a conversation with a model.

            Attributes:
                role (str): The role of the sender (user, assistant, system).
                content (str): The textual content of the message.
                images (dict | list): Optional image content associated with the message.
                timestamp (datetime): The creation timestamp of the message.

            Methods:
                image(file: str, *args, **kwargs): Converts an image file to a dictionary for inclusion in a message.
                __call__(*args, **kwargs): Converts the message object into a dictionary format.
                __str__(*args, **kwargs): Returns a string representation of the message.
                __repr__(*args, **kwargs): Returns a JSON-formatted string of the message attributes.
            """

            class Role:
                USER = "user"
                ASSISTANT = "assistant"
                SYSTEM = "system"

            def __init__(self, role: str, content: str, images: dict | list = None):
                self.timestamp = datetime.datetime.now()
                self.role = (
                    str(role) if role in ["user", "assistant", "system"] else "user"
                )
                self.content = str(content)
                self.images = images
                if self.images is not None:
                    self.images = [images] if isinstance(images, dict) else list(images)

            @staticmethod
            async def image(file: str, *args, **kwargs) -> dict:
                if not os.path.exists(file):
                    return None

                async def read_file():
                    with open(file, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode("utf-8")

                encoded_image = await asyncio.to_thread(read_file)
                file_extension = file.split(".")[-1].lower()

                mime_types = {
                    "png": "image/png",
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "gif": "image/gif",
                    "webp": "image/webp",
                }
                mime_type = mime_types.get(file_extension, "image/png")

                return {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"},
                }

            def __call__(self, *args, **kwargs):
                message = {
                    "role": self.role,
                }
                message["content"] = [{"type": "text", "text": self.content}]
                if self.images is not None:
                    if isinstance(self.images, dict):
                        self.images = [self.images]
                    message["content"].extend(self.images)

                return message

            def __str__(self, *args, **kwargs):
                return f"{self.__class__.__name__}(role={self.role}, content={self.content}, images={len(self.images)}, timestamp={self.timestamp})"

            def __repr__(self, *args, **kwargs):
                return json.dumps(
                    {
                        "class": self.__class__.__name__,
                        "role": self.role,
                        "content": self.content,
                        "images": len(self.images) if self.images is not None else 0,
                        "timestamp": str(self.timestamp),
                    },
                    indent=4,
                )

        class Request:
            """
            ASYNC VERSION

            Handles requests to text-based AI APIs.

            Attributes:
                model (str): The name of the model.
                prompt (str): The input text prompt.
                system (str): System configuration for the request.
                contextual (bool): Whether the request maintains contextual awareness.
                messages (list): List of conversation messages.
                images (list): Optional list of image for vision (openai model only).
                seed (int or str): Random seed for the request.
                jsonMode (bool): Whether the response should be in JSON format.

            Methods:
                __call__(encode: bool, *args, **kwargs): Sends the API request and processes the response.
                __str__(*args, **kwargs): Returns a string representation of the request instance.
                __repr__(*args, **kwargs): Returns a JSON-formatted string of the request attributes.
            """

            def __init__(
                self,
                model: str,
                prompt: str,
                *args,
                system: str = "",
                contextual: bool = False,
                messages: typing.List[dict] = None,
                images: typing.List[dict] = None,
                seed: typing.Union[str, int] = "random",
                jsonMode: bool = False,
                **kwargs,
            ) -> None:
                self.timestamp = datetime.datetime.now()
                self.model = model
                self.prompt = str(prompt)
                self.system = str(system)
                self.contextual = contextual
                self.messages = messages or []
                self.images = images
                self.seed = (
                    random.randint(0, 9999999999) if seed == "random" else int(seed)
                )
                self.jsonMode = jsonMode

            async def __call__(self, encode: bool = False, *args, **kwargs):
                try:
                    async with aiohttp.ClientSession() as session:
                        if self.contextual:
                            messages = [
                                message()
                                if isinstance(message, Async.Text.Message)
                                else message
                                for message in self.messages
                            ]

                            if self.system and (
                                not messages or messages[0]["role"] != "system"
                            ):
                                system_message = Async.Text.Message(
                                    "system", self.system
                                )()
                                messages.insert(0, system_message)

                            if self.prompt is not None:
                                if self.images is not None and len(self.images) > 0:
                                    messages.append(
                                        Async.Text.Message(
                                            "user", self.prompt, self.images
                                        )()
                                    )
                                else:
                                    messages.append(
                                        Async.Text.Message("user", self.prompt)()
                                    )

                            async with session.post(
                                f"https://{API.TEXT.value}/",
                                json={
                                    "model": self.model,
                                    "messages": messages,
                                    "seed": self.seed,
                                    "jsonMode": str(self.jsonMode).lower(),
                                },
                                headers=API.HEADERS.value,
                                timeout=aiohttp.ClientTimeout(total=API.TIMEOUT.value),
                            ) as request:
                                if request.status == 200:
                                    if self.jsonMode:
                                        try:
                                            response = await request.json()
                                        except Exception:
                                            response = await request.text
                                    else:
                                        response = request.text
                                else:
                                    return f"An error occurred: {request.status} - {await request.text()}"
                        else:
                            params = {
                                "model": self.model,
                                "seed": self.seed,
                                "json": str(self.jsonMode).lower(),
                            }
                            if self.system:
                                params["system"] = self.system

                            async with session.get(
                                f"https://{API.TEXT.value}/{self.prompt}",
                                params=params,
                                headers=API.HEADERS.value,
                                timeout=aiohttp.ClientTimeout(total=API.TIMEOUT.value),
                            ) as request:
                                if request.status == 200:
                                    try:
                                        response = await request.json()
                                    except Exception:
                                        response = await request.text()
                                else:
                                    return f"An error occurred: {request.status} - {await request.text()}"

                        if encode:
                            try:
                                response = response.encode("utf-8")
                                response = response.decode("utf-8")
                            except Exception:
                                try:
                                    detection = chardet.detect(await request.read())
                                    response = response.decode(detection["encoding"])
                                except Exception:
                                    pass

                        return response

                except Exception as e:
                    return f"An error occurred: {e}"

            def __str__(self, *args, **kwargs):
                return f"{self.__class__.__name__}(model={self.model}, prompt={self.prompt}, system={self.system}, contextual={self.contextual}, messages={len(self.messages)}, timestamp={self.timestamp})"

            def __repr__(self, *args, **kwargs):
                return json.dumps(
                    {
                        "class": self.__class__.__name__,
                        "model": self.model,
                        "prompt": self.prompt,
                        "system": self.system,
                        "contextual": self.contextual,
                        "messages": len(self.messages),
                        "images": len(self.images) if self.images is not None else 0,
                        "timestamp": str(self.timestamp),
                    },
                    indent=4,
                )

        openai = Model(
            name="openai",
            type="chat",
            censored=True,
            description="OpenAI GPT-4o",
            baseModel=True,
        )

        qwen = Model(
            name="qwen",
            type="chat",
            censored=False,
            description="Qwen 2.5 72B",
            baseModel=True,
        )

        qwen_coder = Model(
            name="qwen-coder",
            type="chat",
            censored=False,
            description="Qwen 2.5 Coder 32B",
            baseModel=True,
        )

        llama = Model(
            name="llama",
            type="chat",
            censored=False,
            description="Llama 3.3 70B",
            baseModel=True,
        )

        mistral = Model(
            name="mistral",
            type="chat",
            censored=False,
            description="Mistral Nemo",
            baseModel=True,
        )

        mistral_large = Model(
            name="mistral-large",
            type="chat",
            censored=False,
            description="Mistral Large (v2)",
            baseModel=True,
        )

        command_r = Model(
            name="command-r",
            type="chat",
            censored=False,
            description="Command-R",
            baseModel=False,
        )

        unity = Model(
            name="unity",
            type="chat",
            censored=False,
            description="Unity with Mistral Large by Unity AI Lab",
            baseModel=False,
        )

        midjourney = Model(
            name="midjourney",
            type="chat",
            censored=True,
            description="Midijourney musical transformer",
            baseModel=False,
        )

        rtist = Model(
            name="rtist",
            type="chat",
            censored=True,
            description="Rtist image generator by @bqrio",
            baseModel=False,
        )

        searchgpt = Model(
            name="searchgpt",
            type="chat",
            censored=True,
            description="SearchGPT with realtime news and web search",
            baseModel=False,
        )

        evil = Model(
            name="evil",
            type="chat",
            censored=False,
            description="Evil Mode - Experimental",
            baseModel=False,
        )

        p1 = Model(
            name="p1",
            type="chat",
            censored=False,
            description="Pollinations 1 (OptiLLM)",
            baseModel=False,
        )
        
        deepseek = Model(
            name="deepseek",
            type="chat",
            censored=True,
            description="DeepSeek-V3",
            baseModel=True
        )

    class Image:
        """
        ASYNC VERSION

        Manages interactions with image-based AI models.

        Attributes:
            model (str): The model's name.
            seed (int or str): Seed for model behavior.
            width (int): The width of the output image.
            height (int): The height of the output image.
            enhance (bool): Whether the prompt should be AI enhanced.
            nologo (bool): Removes logos from output images if True.
            private (bool): Indicates if the request is private from feed.
            safe (bool): Ensures safe content generation (strict NSFW filtering).

        Methods:
            __call__(prompt: str, *args): Sends a prompt to the model and processes the response.
            save(file: str): Saves the response image to a file.
            __str__(*args, **kwargs): Returns a string representation of the Image instance.
            __repr__(*args, **kwargs): Returns a dictionary representation of the Image instance attributes.
        """

        def __init__(
            self,
            model: str = "flux",
            seed: typing.Union[str, int] = "random",
            width: int = 1024,
            height: int = 1024,
            enhance: bool = False,
            nologo: bool = False,
            private: bool = False,
            safe: bool = False,
        ):
            self.timestamp = datetime.datetime.now()
            self.model = model
            self.seed = seed
            self.width = width if isinstance(width, int) else 1024
            self.height = height if isinstance(height, int) else 1024
            self.enhance = enhance if isinstance(enhance, bool) else False
            self.nologo = nologo if isinstance(nologo, bool) else False
            self.private = private if isinstance(private, bool) else False
            self.safe = safe if isinstance(safe, bool) else False

            self.prompt = None
            self.response = None
            self.file = "pollinations-image.png"

        async def __call__(self, prompt: str, *args):
            seed = (
                random.randint(0, 9999999999)
                if self.seed == "random"
                else int(self.seed)
            )

            request = Async.Image.Request(
                model=self.model,
                prompt=prompt,
                seed=seed,
                width=self.width,
                height=self.height,
                enhance=self.enhance,
                nologo=self.nologo,
                private=self.private,
                safe=self.safe,
            )

            self.prompt = prompt
            self.response = await request()

            return self

        async def save(self, file: str = "pollinations-image.png"):
            self.file = file

            if hasattr(self.response, "response"):
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.response.response.url) as response:
                        with open(file, "wb") as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)

            return self

        @staticmethod
        async def models(*args, **kwargs) -> tuple:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"https://{API.IMAGE.value}/models",
                    headers=API.HEADERS.value,
                    timeout=aiohttp.ClientTimeout(total=API.TIMEOUT.value),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return tuple(data)
                    return tuple()

        def __str__(self, *args, **kwargs):
            return f"{self.__class__.__name__}(model={self.model}, seed={self.seed}, width={self.width}, height={self.height}, enhance={self.enhance}, nologo={self.nologo}, private={self.private}, safe={self.safe})"

        def __repr__(self, *args, **kwargs):
            return {
                "model": self.model,
                "seed": self.seed,
                "width": self.width,
                "height": self.height,
                "enhance": self.enhance,
                "nologo": self.nologo,
                "private": self.private,
                "safe": self.safe,
                "timestamp": str(self.timestamp),
            }

        class Request:
            """
            ASYNC VERSION

            Handles requests to image-based AI APIs.

            Attributes:
                model (str): The name of the model.
                prompt (str): The input description or prompt for image generation.
                seed (int or str): Seed for ensuring consistent outputs.
                width (int): The desired width of the output image.
                height (int): The desired height of the output image.
                enhance (bool): Whether the prompt should be AI enhanced.
                nologo (bool): Removes logos from output images if True.
                private (bool): Indicates if the request is private from feed.
                safe (bool): Ensures safe content generation (strict NSFW filtering).
                file (str): The file path for saving the generated image.

            Methods:
                __call__(*args, encode: bool, **kwargs): Sends the image generation request to the API and processes the response.
                save(file: str): Saves the response image to the specified file.
                __str__(*args, **kwargs): Returns a string representation of the request instance.
                __repr__(*args, **kwargs): Returns a JSON-formatted string of the request attributes.
            """

            def __init__(
                self,
                model: str = "flux",
                prompt: str = "",
                seed: typing.Union[str, int] = "random",
                width: int = 1024,
                height: int = 1024,
                enhance: bool = False,
                nologo: bool = False,
                private: bool = False,
                safe: bool = False,
            ):
                self.timestamp = datetime.datetime.now()
                self.model = model
                self.prompt = str(prompt)
                self.seed = random.randint(1, 999999999) if seed == "random" else seed
                self.width = width if isinstance(width, int) else 1024
                self.height = height if isinstance(height, int) else 1024
                self.enhance = enhance if isinstance(enhance, bool) else False
                self.nologo = nologo if isinstance(nologo, bool) else False
                self.private = private if isinstance(private, bool) else False
                self.safe = safe if isinstance(safe, bool) else False

                self.response = None
                self.time = None
                self.params = None

            async def __call__(self, *args, **kwargs):
                try:
                    params = {
                        "safe": str(self.safe).lower(),
                        "seed": self.seed,
                        "width": self.width,
                        "height": self.height,
                        "nologo": str(self.nologo).lower(),
                        "private": str(self.private).lower(),
                        "model": self.model,
                        "enhance": str(self.enhance).lower(),
                    }

                    query_params = "&".join(f"{k}={v}" for k, v in params.items())
                    url = (
                        f"https://{API.IMAGE.value}/prompt/{self.prompt}?{query_params}"
                    )

                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            url=url,
                            headers=API.HEADERS.value,
                            timeout=aiohttp.ClientTimeout(total=API.TIMEOUT.value),
                        ) as response:
                            self.response = response
                            self.time = datetime.datetime.now()
                            self.params = params
                            return self

                except Exception:
                    return self

            def __str__(self, *args, **kwargs):
                return f"{self.__class__.__name__}(model={self.model}, seed={self.seed}, width={self.width}, height={self.height}, enhance={self.enhance}, nologo={self.nologo}, private={self.private}, safe={self.safe})"

            def __repr__(self, *args, **kwargs):
                return {
                    "model": self.model,
                    "seed": self.seed,
                    "width": self.width,
                    "height": self.height,
                    "enhance": self.enhance,
                    "nologo": self.nologo,
                    "private": self.private,
                    "safe": self.safe,
                    "timestamp": str(self.timestamp),
                }

        flux = Model(
            name="flux",
            type="image",
            censored=False,
            description="Flux Image Generative Model",
            baseModel=True,
        )

        flux_realism = Model(
            name="flux-realism",
            type="image",
            censored=False,
            description="Flux Realism Image Generative Model",
            baseModel=False,
        )

        flux_cablyai = Model(
            name="flux-cablyai",
            type="image",
            censored=False,
            description="Flux 1.1 Image Generative Model",
            baseModel=False,
        )

        flux_anime = Model(
            name="flux-anime",
            type="image",
            censored=False,
            description="Flux Anime Image Generative Model",
            baseModel=False,
        )

        flux_3d = Model(
            name="flux-3d",
            type="image",
            censored=False,
            description="Flux 3D Image Generative Model",
            baseModel=False,
        )

        flux_pro = Model(
            name="flux-pro",
            type="image",
            censored=False,
            description="Flux Pro Image Generative Model",
            baseModel=False,
        )

        any_dark = Model(
            name="any-dark",
            type="image",
            censored=False,
            description="Any Dark Image Generative Model",
            baseModel=False,
        )

        turbo = Model(
            name="turbo",
            type="image",
            censored=False,
            description="Turbo Image Generative Model",
            baseModel=True,
        )
