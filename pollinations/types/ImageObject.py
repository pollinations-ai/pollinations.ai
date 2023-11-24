from .. import abc


@abc.resource(deprecated=False)
class ImageObject(abc.ImageProtocol):
    def __init__(
        self, prompt: str, url: str, date: str, content: bin, *args, **kwargs
    ) -> None:
        self.prompt: str = prompt
        self.url: str = url
        self.date: str = date
        self.content: bin = content

    def __repr__(self, *args, **kwargs) -> str:
        return f"ImageObject(prompt={self.prompt}, date={self.date}, url={self.url}, content={len(self.content)})"
