'''
pollinations.types.ImageObject

Classes:
    ImageObject (types.ImageObject): Image object.
'''

from .. import abc


@abc.resource(deprecated=False)
class ImageObject(abc.ImageProtocol):
    '''
    pollinations.ai.types.ImageObject

    Parameters:
        prompt (str): Prompt for the image.
        url (str): URL for the image.
        date (str): Date the image was generated.
        content (binary): Binary content of the image.

    Variables:
        prompt (str): Prompt for the image.
        url (str): URL for the image.
        date (str): Date the image was generated.
        content (binary): Binary content of the image.
    '''''
    def __init__(
        self, prompt: str, url: str, date: str, content: bin, *args, **kwargs
    ) -> None:
        self.prompt: str = prompt
        self.url: str = url
        self.date: str = date
        self.content: bin = content

    def __repr__(self, *args, **kwargs) -> str:
        return f"ImageObject(prompt={self.prompt}, date={self.date}, url={self.url}, content={len(self.content)})"
