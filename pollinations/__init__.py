from .abc import samples
from . import ai as _ai

__version__: str = "0.2.1"


ai: object = _ai

help: object = ai.help

Image: object = ai.Image
Text: object = ai.Text

sample: object = ai.sample
sample_style: object = ai.sample_style
sample_batch: object = ai.sample_batch
