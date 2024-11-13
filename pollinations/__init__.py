__version__: str = "2.1"

import requests
import datetime
import chardet
import base64
import random
import string
import time
import sys
import io
import os

from PIL import Image


TEXT_API: str = "text.pollinations.ai"
IMAGE_API: str = "image.pollinations.ai"
HEADER: dict = {"Content-Type": "application/json"}
ASPECT_RATIOS: dict = {"1:1": (1024, 1024), "3:4": (768, 1024), "16:9": (1024, 576)}

text_default: str = "openai"
openai: str = "openai"
mistral: str = "mistral"
mistral_large: str = "mistral-large"
llama: str = "llama"
karma: str = "karma"
command_r: str = "command-r"
unity: str = "unity"
midjourney: str = "midjourney"
rtist: str = "rtist"
searchgpt: str = "searchgpt"
evil: str = "evil"
qwen_coder: str = "qwen-coder"

image_default: str = "flux"
turbo: str = "turbo"
flux: str = "flux"
flux_realism: str = "flux-realism"
flux_pro: str = "flux-pro"
flux_anime: str = "flux-anime"
flux_3D: str = "flux-3d"
flux_cablyai: str = "flux-cablyai"
any_dark: str = "any-dark"


def text_models(*args, **kwargs) -> tuple:
    models: list = []
    request: requests.Request = requests.get(
        url=f"https://{TEXT_API}/models", headers=HEADER, timeout=30
    )
    for model in request.json():
        models.append(model["name"])
    return tuple(models)


def image_models(*args, **kwargs) -> list:
    request: requests.Request = requests.get(
        url=f"https://{IMAGE_API}/models", headers=HEADER, timeout=30
    )
    return tuple(request.json())


class TextObject(object):
    def __init__(
        self,
        text: str = "",
        prompt: str = "",
        model: str = "",
        messages: list = [],
        params: dict = {},
        *args,
        **kwargs,
    ) -> None:
        self.text: str = str(text)
        self.prompt: str = str(prompt)
        self.model: str = str(model)
        self.messages: list = list(messages)
        self.params: dict = dict(params)
        self.time: str = f"[{datetime.date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

    def __str__(self) -> str:
        return (
            f"TextObject({self.text=}, {self.prompt=}, {self.model=}, {self.time=}, self.messages=[...], self.params="
            + "{...})"
        )

    def __repr__(self) -> repr:
        return repr(self.__str__())


class ImageObject(object):
    def __init__(
        self,
        prompt: str = "",
        negative: str = "",
        model: str = "",
        params: dict = {},
        *args,
        **kwargs,
    ) -> None:
        self.prompt: str = str(prompt)
        self.negative: str = str(negative)
        self.model: str = str(model)
        self.params: dict = dict(params)
        self.time: str = f"[{datetime.date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

    def save(self, file: str="image-output.png", *args, **kwargs) -> object:
        request: requests.Request = requests.get(
            url=self.params["url"],
            headers=HEADER,
            timeout=30,
        )
        Image.open(io.BytesIO(request.content)).save(file)

    def __str__(self) -> str:
        return f"ImageObject({self.prompt=}, {self.negative=}, {self.model=}, {self.params=}, {self.time=})"

    def __repr__(self) -> repr:
        return repr(self.__str__())


class TextModel(object):
    def __init__(
        self,
        frequency_penalty: tuple[int, float] = 0,
        presence_penalty: tuple[int, float] = 0,
        temperature: tuple[int, float] = 0.5,
        top_p: tuple[int, float] = 1,
        model: str = "openai",
        stream: bool = True,
        contextual: bool = False,
        system: str = "",
        *args,
        **kwargs,
    ) -> None:
        self.frequency_penalty: tuple[int, float] = float(frequency_penalty)
        self.presence_penalty: tuple[int, float] = float(presence_penalty)
        self.temperature: tuple[int, float] = float(temperature)
        self.top_p: tuple[int, float] = float(top_p)
        self.model: str = str(model)
        self.stream: bool = bool(stream)
        self.contextual: bool = bool(contextual)
        self.system: str = str(system)
        self.messages: list = list()
        self.limit: list = list([0, 10])
        self.imessage: dict | None = None

        self.system_create: object = lambda _: {"role": "system", "content": str(_)}
        self.user_create: object = lambda _: {"role": "user", "content": str(_)}
        self.assistant_create: object = lambda _: {
            "role": "assistant",
            "content": str(_),
        }

        self.messages.append(self.system_create(self.system))

    def generate(
        self, prompt: str, display: bool = False, *args, **kwargs
    ) -> TextObject:
        prompt: str = str(prompt)
        display: bool = bool(display)

        params: dict = {
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
            "system": self.system,
            "model": self.model,
        }

        if self.limit[0] >= self.limit[1]:
            self.messages.pop(1)

        current_message = {"role": "user"}
        
        if self.imessage:
            current_message["content"] = [
                {"type": "text", "text": prompt},
                self.imessage
            ]
        else:
            current_message["content"] = prompt

        self.messages.append(current_message)
        self.limit[0] += 1

        if self.contextual or any(
            isinstance(msg.get('content'), list) 
            for msg in self.messages 
            if msg['role'] == 'user'
        ):
            params["messages"] = self.messages
            url: str = f"https://{TEXT_API}/"
            request: requests.Request = requests.post(
                url, json=params, headers=HEADER, timeout=30
            )
        else:
            url: str = f"https://{TEXT_API}/{prompt}"
            request: requests.Request = requests.get(
                url,
                params=params,
                headers=HEADER,
                timeout=30,
            )

        if request.status_code == 200:
            try:
                content: str = request.content.decode("utf-8")
            except:
                result: dict = chardet.detect(request.content)
                encoding: str = result['encoding']
                content: str = request.content.decode(encoding)
        else:
            content: str = "An error occurred during generation, try a new prompt."

        self.messages.append({"role": "assistant", "content": content})
        self.limit[0] += 1

        if display:
            for i, character in enumerate(content):
                if i > 0 and content[i - 1] not in set(
                    string.ascii_letters + string.digits + " \t\n"
                ):
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    time.sleep(random.uniform(0.01, 0.05))

                sys.stdout.write(character)
                sys.stdout.flush()

            print()

        image = bool(self.imessage)
        self.imessage = None

        params["url"] = url
        params["image"] = image

        text_object: TextObject = TextObject(
            text=content,
            prompt=prompt,
            model=self.model,
            messages=self.messages,
            params=params,
        )
        return text_object

    def image(self, file: str, *args, **kwargs) -> bool:
        file = str(file)
        if os.path.exists(file):
            with open(file, "rb") as image_file:
                image = base64.b64encode(image_file.read()).decode('utf-8')
                ext = file.split(".")[-1].lower()
                mime_types = {
                    'png': 'image/png',
                    'jpg': 'image/jpeg',
                    'jpeg': 'image/jpeg',
                    'gif': 'image/gif',
                    'webp': 'image/webp'
                }
                mime_type = mime_types.get(ext, 'image/png')
            
            self.imessage = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image}"
                }
            }
            return True
        return False


class ImageModel(object):
    def __init__(
        self,
        model: str = "flux",
        seed: int = 0,
        width: int = 1024,
        height: int = 1024,
        enhance: bool = False,
        nologo: bool = False,
        private: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.model: str = str(model)
        self.seed: int = seed
        self.width: int = int(width)
        self.height: int = int(height)
        self.enhance: bool = bool(enhance)
        self.nologo: bool = bool(nologo)
        self.private: bool = bool(private)

    def generate(
        self,
        prompt: str,
        negative: str = "",
        save: bool = False,
        file: str = "image-output.png",
        *args,
        **kwargs,
    ) -> ImageObject:
        prompt: str = str(prompt)
        save: bool = bool(save)
        file: str = str(file)

        seed: int = self.seed

        if self.seed == "random":
            seed: int = random.randint(0, 9999999999)

        params: str = f"negative={negative}&seed={seed}&width={self.width}&height={self.height}&nologo={self.nologo}&private={self.private}&model={self.model}&enhance={self.enhance}"
        url: str = f"https://{IMAGE_API}/prompt/{prompt}?{params}"
        request: requests.Request = requests.get(
            url=url,
            headers=HEADER,
            timeout=30,
        )
        try:
            image: Image = Image.open(io.BytesIO(request.content))
            if save:
                image.save(file)
            
            params = {
                "seed": seed,
                "width": self.width,
                "height": self.height,
                "nologo": self.nologo,
                "private": self.private,
                "enhance": self.enhance,
                "url": url
            }
            image_object: ImageObject = ImageObject(
                prompt=prompt, negative=negative, model=self.model, params=params
            )
            return image_object
        except:
            return "Image failed to generate, please try again."


def text(
    frequency_penalty: tuple[int, float] = 0,
    presence_penalty: tuple[int, float] = 0,
    temperature: tuple[int, float] = 0.5,
    top_p: tuple[int, float] = 1,
    model: str = text_default,
    stream: bool = True,
    contextual: bool = False,
    system: str = "",
    *args,
    **kwargs,
) -> TextModel:
    return TextModel(
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        temperature=temperature,
        top_p=top_p,
        model=model,
        stream=stream,
        contextual=contextual,
        system=system,
        *args,
        **kwargs,
    )


def image(
    model: str = image_default,
    seed: int = "random",
    width: int = 1024,
    height: int = 1024,
    enhance: bool = False,
    nologo: bool = False,
    private: bool = False,
    *args,
    **kwargs,
) -> ImageModel:
    return ImageModel(
        model=model,
        seed=seed,
        width=width,
        height=height,
        enhance=enhance,
        nologo=nologo,
        private=private,
        *args,
        **kwargs,
    )
