'''
pollinations.types.TextObject

Classes:
    TextObject (types.TextObject): Text object.
'''

from .. import abc


@abc.resource(deprecated=False)
class TextObject(abc.TextProtocol):
    '''
    pollinations.ai.types.TextObject

    Parameters:
        prompt (str): Prompt for the model.
        response (str): Response from the model.

    Variables:
        prompt (str): Prompt for the model.
        response (str): Response from the model.
    '''
    def __init__(self, prompt: str, response: str, *args, **kwargs) -> None:
        self.prompt: str = prompt
        self.response: str = response

    def __repr__(self, *args, **kwargs) -> str:
        return f"TextObject(prompt={self.prompt}, response={self.response})"
