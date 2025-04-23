from __future__ import annotations

from ..types import (
    TextModel,
    Model,
    System,
    Contextual,
    Messages,
    Private,
    Seed,
    ReasoningEffort,
    Tools,
    ToolChoice,
    Voice,
    JsonMode,
    Referrer,
    UseOpenAIEndpoint,
    Images,
    Prompt,
    Output,
    Request,
    Stream,
    StreamData,
    Params,
    Filename,
    PILImage,
    Args,
    Kwargs,
)
from .._utils.check_file import _check_file
from .._utils.format_image import _format_image
from .._utils.create_message import _create_message
from .._utils._models import get_text_models, get_async_text_models
from .._core import (
    BaseClass,
    get_client,
    get_async_client,
    TEXT_API_URI,
    _get_text_request,
    _get_async_text_request,
    _get_stream_text_request,
    _get_async_stream_text_request,
    _get_transcribe_request,
    _get_async_transcribe_request,
)
from ..errors import InvalidOrUnknownPromptError


from typing import Self, Optional, Union, List, Generator, AsyncGenerator


class Text(BaseClass):
    def __init__(
        self: Self,
        model: Optional[Model] = "openai",
        system: Optional[System] = "You are a helpful AI assistant.",
        contextual: Optional[Contextual] = False,
        messages: Optional[Messages] = [],
        private: Optional[Private] = False,
        seed: Optional[Seed] = "random",
        reasoning_effort: Optional[ReasoningEffort] = "medium",
        tools: Optional[Tools] = [],
        tool_choices: Optional[ToolChoice] = [],
        voice: Optional[Voice] = None,
        json_mode: Optional[JsonMode] = False,
        referrer: Optional[Referrer] = "pollinations.py",
        openai_endpoint: Optional[UseOpenAIEndpoint] = False,
        *any_kwargs_will_be_passed_in_request: Args,
        **kwargs: Kwargs,
    ) -> None:
        self._client = get_client(TEXT_API_URI)
        self._async_client = get_async_client(TEXT_API_URI)
        
        self.status = "DONE"

        self.model = model
        self.system = system
        self.contextual = contextual
        self.messages = messages
        self.private = private
        self.seed = seed
        self.reasoning_effort = reasoning_effort
        self.tools = tools
        self.tool_choices = tool_choices
        self.voice = voice
        self.json_mode = json_mode
        self.referrer = referrer
        self.openai_endpoint = openai_endpoint

        self.images: Images = None
        self.prompt: Prompt = None
        self.response: Output = None
        self.request: Request = None

        if self.system and not any(m.get("role") == "system" for m in self.messages):
            self.messages.insert(0, _create_message("system", self.system))


        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(
        self: Self,
        prompt: Optional[Prompt] = None,
        *any_kwargs_will_be_passed_in_request: Args,
        stream: Optional[Stream] = False,
        **kwargs: Kwargs,
    ) -> Output:
        return self.Generate(
            prompt,
            *any_kwargs_will_be_passed_in_request,
            stream=stream,
            **kwargs,
        )

    def Generate(
        self: Self,
        prompt: Optional[Prompt] = None,
        *any_kwargs_will_be_passed_in_request: Args,
        stream: Optional[Stream] = False,
        **kwargs: Kwargs,
    ) -> Output:
        self.status = "RUNNING"
        prompt = self._check(prompt)

        if self.contextual:
            self.messages.append(_create_message("user", prompt))

        params = self._setup(prompt)


        if stream:

            def _generator() -> Generator[StreamData]:
                text = ""
                for chunk in _get_stream_text_request(
                    self._client, params, **kwargs
                ):
                    text += chunk
                    yield chunk
                self.response = text
                if self.contextual:
                    self.messages.append(
                        _create_message("assistant", self._decode(text))
                    )
                    
                self.status = "DONE"

            return _generator()
        else:
            self.request = _get_text_request(self._client, params, **kwargs)
            self.response = self._decode(self.request.content)
            if self.contextual:
                self.messages.append(
                    _create_message("assistant", self.response)
                )

            self.status = "DONE"
            return self.response

    async def Async(
        self: Self,
        prompt: Optional[Prompt] = None,
        *any_kwargs_will_be_passed_in_request: Args,
        stream: Optional[Stream] = False,
        **kwargs: Kwargs,
    ) -> Output:
        self.status = "RUNNING"
        prompt = self._check(prompt)

        if self.contextual:
            self.messages.append(_create_message("user", prompt))

        params = self._setup(prompt)

        if stream:

            async def _generator() -> AsyncGenerator[StreamData]:
                text = ""
                async for chunk in await _get_async_stream_text_request(
                    self._async_client, params, **kwargs
                ):
                    text += chunk
                    yield chunk
                self.response = text
                if self.contextual:
                    self.messages.append(
                        _create_message("assistant", self._decode(text))
                    )
                self.status = "DONE"

            return _generator()
        else:
            self.request = await _get_async_text_request(
                self._async_client, params, **kwargs
            )
            self.response = self._decode(self.request.content)
            if self.contextual:
                self.messages.append(
                    _create_message("assistant", self.response)
                )

            self.status = "DONE"
            return self.response

    def Transcribe(
        self: Self,
        file: Filename,
        *any_kwargs_will_be_passed_in_request: Args,
        **kwargs: Kwargs,
    ) -> Output:
        self.status = "RUNNING"
        params: Params = {"file": file, "seed": self.seed}
        request = _get_transcribe_request(
            self._client,
            params,
            *any_kwargs_will_be_passed_in_request,
            **kwargs,
        )
        self.status = "DONE"
        return request

    async def TranscribeAsync(
        self: Self,
        file: Filename,
        *any_kwargs_will_be_passed_in_request: Args,
        **kwargs: Kwargs,
    ) -> Output:
        self.status = "RUNNING"
        params: Params = {"file": file, "seed": self.seed}
        request = await _get_async_transcribe_request(
            self._async_client,
            params,
            *any_kwargs_will_be_passed_in_request,
            **kwargs,
        )
        self.status = "DONE"
        return request

    def Image(
        self: Self,
        file: Union[Filename, List[Filename]],
        *args: Args,
        **kwargs: Kwargs,
    ) -> PILImage:
        files = [file] if isinstance(file, Filename) else file
        self.images = [_format_image(f) for f in files if f and _check_file(f)]

    @staticmethod
    def Models() -> List[TextModel]:
        return get_text_models()

    @staticmethod
    async def ModelsAsync() -> List[TextModel]:
        return await get_async_text_models()

    def _check(self: Self, prompt: Optional[Prompt] = None) -> Prompt:
        if prompt:
            return prompt

        try:
            last = self.messages[-1]["content"]
            return last["text"] if isinstance(last, dict) else last
        except Exception:
            return InvalidOrUnknownPromptError(
                InvalidOrUnknownPromptError.DefaultMessage
            )

    def _setup(self: Self, prompt: Prompt) -> Params:
        params = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
            and k not in {"images", "prompt", "response", "request", "system"}
        }

        if self.contextual:
            params["messages"] = self.messages
        else:
            params["messages"] = self.messages + [_create_message("user", prompt)]

        if self.system:
            params["__system"] = self.system
        if self.images:
            params["__images"] = self.images
        params["__prompt"] = prompt or " " 
        self.images = []
        return params


    @staticmethod
    def _decode(content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except Exception:
            return str(content)
