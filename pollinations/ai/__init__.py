import random
from .. import abc
from .. import ext
from ..types.ImageModel import ImageModel
from ..types.TextModel import TextModel

Image: ImageModel = ImageModel
Text: TextModel = TextModel

samples: list = ext.samples
styles: dict = ext.styles

realistic: str = ext.realistic
cartoon: str = ext.cartoon
anime: str = ext.anime
logo: str = ext.logo

sample_style: object = ext.sample_style
sample: object = ext.sample
sample_batch: object = ext.sample_batch


@abc.resource(deprecated=True)
def help(*args, **kwargs) -> str:
    help_return: str = (
        """
  sample(): returns 1 random sample prompt

  sample_style(): returns a style of art (realistic, cartoon, anime, logo))

  sample_batch(size: int): returns size batch of random sample prompts

  Image(save_file: str (OPTIONAL)): inialize the ai.Image

  Image.set_filter(filter: list): set the filter for list of backlisted words

  Image.generate(prompt: str): generate an image from a prompt

  Image.generate_batch(prompts: list): generate an image from a batch of prompts

  Image.save(save_file: str (OPTIONAL)): save the image to a file

  Image.load(load_file: str (OPTIONAL)): load the image from a file

  Image.image(): return the image object

  Text(save_file: str (OPTIONAL)): inialize the ai.Text

  Text.chat(prompt: str): chat with the ai and return the response

  """
        ""
    )
    return help_return


BANNED_WORDS: list = abc.BANNED_WORDS
