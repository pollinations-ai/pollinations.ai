import requests
from .. import abc

@abc.resource(deprecated=False)
class Image:
  def __init__(self, save_file: str='tkr-Image.jpg', *args, **kwargs) -> None:
      self.__base: str = 'image.pollinations'
      self.save_file: str = save_file
      self.prompt: str = None
      self.filter: list = []
      self.is_filtered: bool = False

  def __repr__(self, *args, **kwargs) -> str:
    return f"Image(save_file={self.save_file})"

  @abc.resource(deprecated=False)
  def set_filter(self, filter: list, *args, **kwargs) -> object:
    self.filter: list = filter
    return self

  @abc.resource(deprecated=False)
  def generate(self, prompt: str, *args, **kwargs) -> str:
      words: list = prompt.split(' ')
      for word in words:
        if word in self.filter:
          self.is_filtered: bool = True
          return Exception(f"ai.Image >>> InvalidPrompt (filtered)")

      self.prompt: str = prompt
      request = requests.get(f'{abc.proto}{self.__base}{abc.ai}{prompt}')
      self.data: abc.ImageObject = abc.ImageObject(prompt, request.url, request.headers['Date'], content=request.content)
      self.data.save: object = self.save

      return self.data

  @abc.resource(deprecated=False)
  def generate_batch(self, prompts: list, save: bool=False, path: str = None, naming: str='counter', *args, **kwargs) -> list:
      self.prompts: list = prompts
      self.data: list = []
      counter: int = 1

      for prompt in prompts:
          words: list = prompt.split(' ')
          for word in words:
            if word in self.filter:
              self.is_filtered: bool = True
              return Exception(f"ai.Image >>> InvalidPrompt (filtered)")
          request = requests.get(f'{abc.proto}{self.__base}{abc.ai}{prompt}')
          image = abc.ImageObject(prompt, request.url, request.headers['Date'], content=request.content)
          image.save: object = self.save
          self.data.append(image)

          if save:
              if naming == 'counter': file_name: str = counter
              else: file_name: str = prompt
              with open(f'{path if path else ""}/batch{file_name}-pollinations.jpg', 'wb') as handler:
                  handler.write(image.content)

          counter += 1

      return self.data

  @abc.resource(deprecated=False)
  def save(self, save_file: str=None, *args, **kwargs) -> abc.ImageObject:
    if not self.is_filtered:
      if save_file is None:
        save_file = self.save_file

      with open(save_file, 'wb') as handler:
        handler.write(self.data.content)

      return self.data
    else:
      return Exception(f"ai.Image >>> Cannot Save (filtered)")

  @abc.resource(deprecated=False)
  def load(self, load_file: str=None, *args, **kwargs) -> str:
    if load_file is None:
      load_file = self.save_file

    with open(load_file, 'rb') as handler:
      return handler.read()

  @abc.resource(deprecated=False)
  def image(self, *args, **kwargs) -> abc.ImageObject:
    return self.data

