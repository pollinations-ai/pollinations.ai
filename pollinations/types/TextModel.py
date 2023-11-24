import google.generativeai as palm
from .. import abc
from .TextObject import TextObject


@abc.resource(deprecated=False)
class TextModel:
    def __init__(self, name: str = "pollinations.ai", *args, **kwargs) -> None:
        self.name: str = name
        self.data: object = object
        palm.configure(api_key=abc.site.split("+ai/")[1].split("/")[0])

    @abc.resource(deprecated=True)
    def chat(self, prompt: str, *args, **kwargs) -> str:
        response: str = palm.chat(prompt=prompt).last
        self.data: TextObject = TextObject(prompt=prompt, response=response)
        return self.data
