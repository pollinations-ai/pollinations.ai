from .abc import samples

__version__ = '0.1.4'

import random

class Sample:
  @property
  def prompt(self) -> str:
    return random.choice(samples)

  def batch(self, size: int=10, *args, **kwargs) -> list:
    return random.choices(samples, k=size)

def main(*args, **kwargs) -> str:
  pollinations_ai_info: str = """
  [[ pollinations.ai ]]

  Architect:
    pollinations
      file: __init__.py

      folders:
        - abc
        - ai
        - ext

      [[ ai usage ]]
      ```python

      import pollinations.ai as ai

      ImageAi = ai.Image()
      ImageAi.generate(
          ai.sample()
      )
      
      ImageAi.save()
      ```
  """
  print(pollinations_ai_info)
  return pollinations_ai_info

@abc.resource(deprecated=True)
def help(*args, **kwargs) -> str:
  help_return: str = """
  sample(): returns 1 random sample prompt

  sample_batch(size: int): returns size batch of random sample prompts

  Image(save_file: str (OPTIONAL)): inialize the ai.Image

  Image.set_filter(filter: list): set the filter for list of backlisted words

  Image.generate(prompt: str): generate an image from a prompt

  Image.generate_batch(prompts: list): generate an image from a batch of prompts

  Image.save(save_file: str (OPTIONAL)): save the image to a file

  Image.load(load_file: str (OPTIONAL)): load the image from a file

  Image.image(): return the image object

  """""
  return help_return
