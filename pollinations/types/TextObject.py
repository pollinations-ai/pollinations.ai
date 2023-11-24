from .. import abc


@abc.resource(deprecated=False)
class TextObject(abc.TextProtocol):
    def __init__(self, prompt: str, response: str, *args, **kwargs) -> None:
        self.prompt: str = prompt
        self.response: str = response

    def __repr__(self, *args, **kwargs) -> str:
        return f"TextObject(prompt={self.prompt}, response={self.response})"
