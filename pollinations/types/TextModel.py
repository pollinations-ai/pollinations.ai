"""
pollinations.types.TextModel

Classes:
    TextModel (types.TextModel): Text-to-text generative AI model.
    TextObject (types.TextObject): Text object.
"""

import google.generativeai as palm
from .. import abc
from .TextObject import TextObject


@abc.resource(deprecated=False)
class TextModel:
    """
    pollinations.ai.types.TextModel

    Parameters:
        name (str): Name of the model.

    Variables:
        name (str): Name of the model.

    Functions:
        chat(TextObject, prompt: str): Chat with the model.
    """

    def __init__(self, name: str = "pollinations.ai", *args, **kwargs) -> None:
        self.name: str = name
        self.data: object = object
        palm.configure(api_key=abc.site.split("+ai/")[1].split("/")[0])

    def __repr__(self, *args, **kwargs) -> str:
        return f"Text(name={self.name})"

    @abc.resource(deprecated=True)
    def chat(self, prompt: str, *args, **kwargs) -> str:
        """
        pollinations.ai.types.TextModel.chat

        Parameters:
            prompt (str): Prompt for the model.

        Return:
            TextObject (class): Returns the TextObject for the model response.
        """
        response: str = palm.chat(prompt=prompt).last
        self.data: TextObject = TextObject(prompt=prompt, response=response)
        return self.data
