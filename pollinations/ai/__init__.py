import random
from ..ext import Image
from .. import abc

models: dict = {
  'tti-safe.v3': 'No banned words allowed in prompt, raises Exception',
  'tti-unsafe.v3': 'No filter for prompts, does not raise Exception'
}

@abc.resource(deprecated=True)
def get_models(*args, **kwargs):
  print(models)
  return models

samples: list = abc.samples
styles: dict = {
  'realistic': 'realistic, realism, real life, ultra realistic, high quality, real',
  'cartoon': 'cartoony, cartoon, cartoonish',
  'anime': 'anime, anime art, anime style',
  'logo': 'logo, logo design, logo graphic design, logo digital art',
}

realistic: str = styles.get('realistic')
cartoon: str = styles.get('cartoon')
anime: str = styles.get('anime')
logo: str = styles.get('logo')

@abc.resource(deprecated=False)
def sample_style(*args, **kwargs):
  return styles.get(random.choice(list(styles.keys())))

@abc.resource(deprecated=False)
def sample(*args, **kwargs) -> str:
  return f'prompt: {random.choice(samples)}, details: ({sample_style()})'

@abc.resource(deprecated=False)
def sample_batch(size: int, *args, **kwargs) -> str:
  return [sample() for iter in range(size)]

@abc.resource(deprecated=True)
def help(*args, **kwargs) -> str:
  help_return: str = """
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
  
  """""
  return help_return

BANNED_WORDS: list = abc.BANNED_WORDS
