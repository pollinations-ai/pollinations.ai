__version__ = "2.3"

import requests
import datetime
import chardet
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
    TEXT = "text.pollinations.ai"
    IMAGE = "image.pollinations.ai"
    HEADERS = {"Content-Type": "application/json"}
    TIMEOUT = 60


class Model(object):
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
                    try:
                        response = request.json()
                    except Exception:
                        response = request.text

                    if encode:
                        try:
                            response = response.encode("utf-8")
                            response = response.decode("utf-8")
                        except Exception:
                            detection = chardet.detect(request.content)
                            response = response.decode(detection["encoding"])

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


class Image(object):
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
