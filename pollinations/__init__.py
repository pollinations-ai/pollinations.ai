__version__ = "2.2"

from datetime import date
from typing import Type, TypeVar, Optional, List, Dict, Union, Tuple
import requests
import chardet
import base64
import random
import string
import time
import sys
import os

T = TypeVar('T', bound='_ModelBase')

class APIConfig:
    TEXT_ENDPOINT = "text.pollinations.ai"
    IMAGE_ENDPOINT = "image.pollinations.ai"
    HEADERS = {"Content-Type": "application/json"}
    REQUEST_TIMEOUT = 50

class _ModelBase:
    name: str
    type: str
    censored: bool
    description: str
    base_model: bool

    def info(self) -> Dict[str, Union[str, bool]]:
        return {
            "name": self.name,
            "type": self.type,
            "censored": self.censored,
            "description": self.description,
            "base_model": self.base_model,
        }

    def __call__(self, *args, **kwargs) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

def _create_model(
    name: str,
    model_type: str,
    censored: bool,
    description: str,
    base_model: bool
) -> Type[_ModelBase]:
    return type(
        name,
        (_ModelBase,),
        {
            "name": name,
            "type": model_type,
            "censored": censored,
            "description": description,
            "base_model": base_model,
        },
    )

class Text:
    class Object:
        def __init__(
            self, 
            text: str = "",
            prompt: str = "",
            model: str = "",
            messages: List[Dict] = None,
            params: Dict = None,
            time: str = "",
            error: str = "",
            image: bool = False,
        ):
            self.text = text
            self.response = text
            self.prompt = prompt
            self.model = model
            self.messages = messages or []
            self.params = params or {}
            self.time = time
            self.error = error
            self.image = image

        def __str__(self) -> str:
            return (
                f"Text.Object(text='{self.text}', prompt='{self.prompt}', "
                f"model='{self.model}', time='{self.time}', messages=[...], params={{...}})"
            )

        def __repr__(self) -> str:
            return self.__str__()

    def __init__(
        self,
        model: str = "openai",
        contextual: bool = False,
        seed: Union[str, int] = "random",
        system: str = "",
        limit: int = 20,
    ):
        self.model = model
        self.contextual = contextual
        self.seed = seed
        self.system = system
        self.imessage: Optional[Dict] = None
        self.messages: List[Dict] = []
        self._initialize_messages()
        self.limit = [0, limit]
        self._update_timestamp()
        self.error_message = "An error occurred during generation."
        self.error = None

    def _initialize_messages(self) -> None:
        if self.system:
            self.messages = [{"role": "system", "content": self.system}]
        else:
            self.messages = []

    def _update_timestamp(self) -> None:
        self.time = f"[{date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

    def generate(self, prompt: str, display: bool = False) -> Object:
        self._update_timestamp()
        prompt = str(prompt)
        seed = random.randint(0, 9999999999) if self.seed == "random" else self.seed
        
        params = {
            "system": self.system,
            "model": self.model,
            "seed": seed,
        }

        if self.limit[0] >= self.limit[1] and len(self.messages) > 1:
            self.messages = [self.messages[0]] + self.messages[3:]

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

        try:
            if self.contextual or any(
                isinstance(msg.get('content'), list) 
                for msg in self.messages 
                if msg['role'] == 'user'
            ):
                params["messages"] = self.messages
                response = requests.post(
                    url=f"https://{APIConfig.TEXT_ENDPOINT}/",
                    json=params,
                    headers=APIConfig.HEADERS,
                    timeout=APIConfig.REQUEST_TIMEOUT
                )
            else:
                response = requests.get(
                    url=f"https://{APIConfig.TEXT_ENDPOINT}/{prompt}",
                    params=params,
                    headers=APIConfig.HEADERS,
                    timeout=APIConfig.REQUEST_TIMEOUT
                )

            if response.status_code == 200:
                try:
                    content: str = response.content.decode("utf-8")
                except Exception:
                    result: dict = chardet.detect(response.content)
                    encoding: str = result['encoding']
                    content: str = response.content.decode(encoding)
            else:
                content = self.error_message

            self.messages.append({"role": "assistant", "content": content})
            self.limit[0] += 1

            if display:
                self._display_text(content)

            image_included = bool(self.imessage)
            self.imessage = None

            return Text.Object(
                text=content,
                prompt=prompt,
                model=self.model,
                messages=self.messages,
                params=params,
                time=self.time,
                error="",
                image=image_included
            )

        except Exception as e:
            error_msg = f"Generation error: {str(e)}"
            return Text.Object(
                text=error_msg,
                prompt=prompt,
                model=self.model,
                messages=self.messages,
                params=params,
                time=self.time,
                error=str(e),
                image=False
            )

    def _display_text(self, content: str) -> None:
        for i, char in enumerate(content):
            delay = (0.1, 0.3) if i > 0 and content[i - 1] not in set(
                string.ascii_letters + string.digits + " \t\n"
            ) else (0.01, 0.05)
            
            time.sleep(random.uniform(*delay))
            sys.stdout.write(char)
            sys.stdout.flush()
        print()

    def image(self, file: str) -> bool:
        if not os.path.exists(file):
            return False

        with open(file, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
            file_extension = file.split(".")[-1].lower()
            
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(file_extension, 'image/png')
        
        self.imessage = {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{encoded_image}"
            }
        }
        return True

    @staticmethod
    def models() -> tuple:
        response = requests.get(
            url=f"https://{APIConfig.TEXT_ENDPOINT}/models",
            headers=APIConfig.HEADERS,
            timeout=APIConfig.REQUEST_TIMEOUT
        )
        if response.status_code == 200:
            return tuple(model["name"] for model in response.json())
        return tuple()

    openai = _create_model("openai", "chat", True, "OpenAI GPT-4", True)
    qwen = _create_model("qwen", "chat", False, "Qwen 2.5 72B", True)
    qwen_coder = _create_model("qwen-coder", "chat", False, "Qwen 2.5 Coder 32B", True)
    llama = _create_model("llama", "chat", False, "Llama 3.3 70B", True)
    mistral = _create_model("mistral", "chat", False, "Mistral Nemo", True)
    mistral_large = _create_model("mistral-large", "chat", False, "Mistral Large (v2)", True)
    command_r = _create_model("command-r", "chat", False, "Command-R", False)
    unity = _create_model("unity", "chat", False, "Unity with Mistral Large by Unity AI Lab", False)
    midijourney = _create_model("midijourney", "chat", True, "Midijourney musical transformer", False)
    rtist = _create_model("rtist", "chat", True, "Rtist image generator by @bqrio", False)
    searchgpt = _create_model("searchgpt", "chat", True, "SearchGPT with realtime news and web search", False)
    evil = _create_model("evil", "chat", False, "Evil Mode - Experimental", False)
    p1 = _create_model("p1", "chat", False, "Pollinations 1 (OptiLLM)", False)

class Image:
    class Object:
        def __init__(
            self,
            prompt: str = "",
            model: str = "",
            safe: str = "",
            params: Dict = None,
            time: str = "",
            error: str = "",
            url: str = "",
        ):
            self.prompt = prompt
            self.model = model
            self.safe = safe
            self.params = params or {}
            self.time = time
            self.error = error
            self.url = url
            self._update_timestamp()

        def _update_timestamp(self) -> None:
            self.time = f"[{date.today().strftime('%Y-%m-%d')}] {time.strftime('%H:%M:%S')}"

        def save(self, file: str = "image-output.png") -> bool:
            try:
                if not self.error and self.params.get("url"):
                    response = requests.get(
                        url=self.params["url"],
                        headers=APIConfig.HEADERS,
                        timeout=APIConfig.REQUEST_TIMEOUT,
                        stream=True
                    )
                    if response.status_code == 200:
                        with open(file, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        return True
                return False
            except Exception:
                return False

        def __str__(self) -> str:
            return (
                f"Image.Object(prompt='{self.prompt}', safe='{self.safe}', "
                f"model='{self.model}', time='{self.time}', params={{...}})"
            )

        def __repr__(self) -> str:
            return self.__str__()

    def __init__(
        self,
        model: str = "flux",
        seed: Union[str, int] = "random",
        width: int = 1024,
        height: int = 1024,
        enhance: bool = False,
        nologo: bool = False,
        private: bool = False,
    ):
        self.model = model
        self.seed = seed
        self.width = width
        self.height = height
        self.enhance = enhance
        self.nologo = nologo
        self.private = private

    def generate(
        self,
        prompt: str,
        safe: str = "",
        save: bool = False,
        file: str = "image-output.png"
    ) -> Object:
        try:
            seed = random.randint(0, 9999999999) if self.seed == "random" else int(self.seed)
            
            params = {
                "safe": safe,
                "seed": seed,
                "width": self.width,
                "height": self.height,
                "nologo": self.nologo,
                "private": self.private,
                "model": self.model,
                "enhance": self.enhance
            }

            query_params = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"https://{APIConfig.IMAGE_ENDPOINT}/prompt/{prompt}?{query_params}"
            
            response = requests.get(
                url=url,
                headers=APIConfig.HEADERS,
                timeout=APIConfig.REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                params["url"] = url
                image_obj = Image.Object(
                    prompt=prompt,
                    safe=safe,
                    model=self.model,
                    params=params,
                )
                
                if save:
                    with open(file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                return image_obj
            else:
                return Image.Object(
                    prompt=prompt,
                    safe=safe,
                    model=self.model,
                    error=f"Server error: {response.status_code}",
                    url=url
                )

        except Exception as e:
            return Image.Object(
                prompt=prompt,
                safe=safe,
                model=self.model,
                error=f"Generation error: {str(e)}",
                url=url
            )

    @staticmethod
    def models() -> Tuple[str, ...]:
        response = requests.get(
            url=f"https://{APIConfig.IMAGE_ENDPOINT}/models",
            headers=APIConfig.HEADERS,
            timeout=APIConfig.REQUEST_TIMEOUT
        )
        if response.status_code == 200:
            return tuple(response.json())
        return tuple()

    flux = _create_model("flux", "image", False, "Flux Model", True)
    flux_realism = _create_model("flux-realism", "image", False, "Flux Realism Style", True)
    flux_cablyai = _create_model("flux-cablyai", "image", False, "Flux 1.1 Model", True)
    flux_anime = _create_model("flux-anime", "image", False, "Flux Anime Style", True)
    flux_3d = _create_model("flux-3d", "image", False, "Flux 3D Style", True)
    any_dark = _create_model("any-dark", "image", False, "Any Dark Style", True)
    flux_pro = _create_model("flux-pro", "image", False, "Flux Pro Model", True)
    turbo = _create_model("turbo", "image", False, "Turbo Model", True)
