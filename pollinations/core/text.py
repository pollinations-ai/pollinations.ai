from __future__ import annotations

from pollinations._types import List, Union, Dict, Any, Optional
from pollinations._constants import TEXT_API_URI
from pollinations.utils._request import (
    get_client,
    get_async_client,
    get_request,
    get_async_request,
    get_audio_request,
    get_audio_async_request,
    Stream,
)
from pollinations.utils._safe import Safe
from pollinations.utils._models import text_models
from pollinations.utils._image import _safe_check, _format_image


__all__ = ["Text"]


class Role:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Text:
    __all__ = [
        "__init__",
        "__call__",
        "__repr__",
        "__str__",
        "image",
        "models",
        "Async",
        "Transcribe",
        "TranscribeAsync",
        "Message",
    ]

    @Safe.auto(
        model=(str, "openai"),
        system=str,
        contextual=(bool, False),
        messages=(list),
        private=(bool, False),
        reasoning_effort=(str, "medium"),
        tools=list,
        tool_choices=list,
        seed=(Union[int, str], "random"),
        json_mode=(bool, False),
        referrer=(str, "pollinations.py"),
        openai_endpoint=(bool, False),
        voice=str,
    )
    def __init__(
        self,
        model: str = "openai",
        system: str = "You are a helpful assistant.",
        contextual: bool = False,
        messages: Optional[List[Dict[str, Any]]] = None,
        private: bool = False,
        seed: Union[int, str] = "random",
        reasoning_effort: Optional[str] = "medium",
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choices: Optional[List[str]] = None,
        voice: str = None,
        json_mode: bool = False,
        referrer: str = "pollinations.py",
        openai_endpoint: bool = False,
        *any_kwargs_will_be_passed_in_request: Any,
        **kwargs,
    ) -> None:
        self._client = get_client(TEXT_API_URI)
        self._async_client = get_async_client(TEXT_API_URI)

        self.model = model
        self.system = system
        self.contextual = contextual
        self.messages = messages or []
        self.private = private
        self.seed = seed
        self.reasoning_effort = (
            reasoning_effort
            if reasoning_effort in ["low", "medium", "high"]
            else "medium"
        )
        self.tools = tools
        self.tool_choices = tool_choices
        self.voice = voice
        self.json_mode = json_mode
        self.referrer = referrer
        self.openai_endpoint = openai_endpoint

        if self.system:
            self.messages.insert(0, self.Message(Role.SYSTEM, self.system)())

        self.images: Optional[List[Dict[str, Any]]] = None
        self.prompt: Optional[str] = None
        self.response: Optional[str] = None
        self.request: Optional[Any] = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(
        self, prompt: Optional[str] = None, stream: bool = False
    ) -> Union[str, Any]:
        self.prompt = self._check(prompt)
        params = self._setup(self.prompt)

        self.images = None

        if stream:

            def generator() -> Any:
                response_text = ""
                for chunk in Stream.get_request(self._client, params):
                    response_text += chunk
                    yield chunk
                self.response = response_text
                self.messages.append(self.Message(Role.ASSISTANT, response_text)())

            return generator()
        else:
            self.request = get_request(self._client, params)
            self.response = self._decode(self.request.content)
            self.messages.append(self.Message(Role.ASSISTANT, self.response)())
            return self.response

    async def Async(
        self, prompt: Optional[str] = None, stream: bool = False
    ) -> Union[str, Any]:
        self.prompt = self._check(prompt)
        params = self._setup(self.prompt)

        self.images = None

        if stream:

            async def async_generator() -> Any:
                response_text = ""
                async for chunk in await Stream.get_async_request(
                    self._async_client, params
                ):
                    response_text += chunk
                    yield chunk
                self.response = response_text
                self.messages.append(self.Message(Role.ASSISTANT, response_text)())

            return async_generator()
        else:
            self.request = await get_async_request(self._async_client, params)
            self.response = self._decode(self.request.content)
            self.messages.append(self.Message(Role.ASSISTANT, self.response)())
            return self.response

    def Transcribe(
        self, file: str, *any_kwargs_will_be_passed_in_request: Any, **kwargs
    ):
        return get_audio_request(
            get_client(TEXT_API_URI + "openai"), {"file": file}, **kwargs
        )

    async def TranscribeAsync(
        self, file: str, *any_kwargs_will_be_passed_in_request: Any, **kwargs
    ):
        return await get_audio_async_request(
            get_async_client(TEXT_API_URI + "openai"), {"file": file}, **kwargs
        )

    def image(self, file: Union[str, List[str]]) -> None:
        files = [file] if isinstance(file, str) else file
        self.images = [self.Message.image(f) for f in files if f and _safe_check(f)]

    def _check(self, prompt: Optional[str]) -> str:
        if prompt:
            return prompt
        try:
            last = self.messages[-1]["content"]
            return last["text"] if isinstance(last, dict) else last
        except Exception:
            return " "

    def _setup(self, prompt: str) -> Dict[str, Any]:
        params = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
            and k not in {"images", "prompt", "response", "request", "system"}
        }

        if not self.contextual:
            params["_prompt"] = prompt
            if self.system:
                params["_system"] = self.system
            if self.images:
                params["_images"] = self.images
        else:
            if prompt:
                self.messages.append(self.Message(Role.USER, prompt, self.images)())
            params["messages"] = self.messages

        return params

    @staticmethod
    def _decode(content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except Exception:
            return str(content)

    @staticmethod
    def models() -> List:
        return text_models()

    def __repr__(self) -> str:
        def _short(value):
            if isinstance(value, list):
                return f"<{len(value)} items>"
            elif isinstance(value, str) and len(value) > 50:
                return f"{value[:50]}... [{len(value) - 50} more]"
            return repr(value)

        items = []

        for k, v in self.__dict__.items():
            if k in {"_client", "_async_client"}:
                continue
            if k == "images" and v is not None:
                items.append(f"{k}={len(v)}")
            elif k == "messages" and v is not None:
                items.append(f"{k}={len(v)}")
            elif k == "system":
                items.append(f"{k}={_short(v)}")
            else:
                items.append(f"{k}={_short(v)}")

        return f"{self.__class__.__name__}({', '.join(items)})"

    def __str__(self) -> str:
        return self.response if self.response not in [None, ""] else self.__repr__()

    class Message:
        @Safe.auto(role=str, content=str)
        def __init__(
            self,
            role: str,
            content: str,
            images: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        ) -> None:
            self.role = role
            self.content = content
            self.images = images

        def __call__(self) -> Dict[str, Any]:
            message = {
                "role": self.role,
                "content": [{"type": "text", "text": self.content}],
            }
            if self.images:
                if isinstance(self.images, dict):
                    self.images = [self.images]
                message["content"].extend(self.images)
            return message

        @staticmethod
        @Safe.auto(file=str)
        def image(file: str) -> Optional[Dict[str, Any]]:
            return _format_image(file)
