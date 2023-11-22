<div id="header">
  <img src="https://i.ibb.co/p049Y5S/86964862.png" width="50"/>   <img src="https://i.ibb.co/r6JZ336/sketch1700556567238.png" width="250">
</div>

# [pollinations.ai - Image Generation](https://pypi.org/project/pollinations.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/toolkitr/tkr/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20-blue)](https://www.python.org/downloads/)

```
pollinations.ai: (https://pollinations.ai/)

This is a WRAPPER designed for easy text-image generation.
```

# CHANGELOG V0.1.8

## Installing
```shell
# Linux/macOS
python3 -m pip install -U pollinations.ai

# Windows
py -3 -m pip install -U pollinations.ai
```

## Added
```
+ pollinations.ai.models: dict
+ pollinations.ai.samples: list
+ pollinations.ai.styles: dict

+ pollinations.ai.realistic: str
+ pollinations.ai.cartoon: str
+ pollinations.ai.anime: str
+ pollinations.ai.logo: str

+ pollinations.ai.sample() >> Generates a random prompt from .ai.samples and a random style from .ai.styles.
+ pollinations.ai.sample_style() >> Gets a random style from .ai.styles.
+ pollinations.ai.sample_batch(size: int) >> Generates a batch of <size> prompts with styles.
```

## Image Model
```
+ pollinations.ai.Image.filter: list
+ pollinations.ai.Image.set_filter(filter: list)

+ pollinations.ai.Image.generate(prompt: str) >> Generates an image from a given prompt.
+ pollinations.ai.Image.generate_batch(prompts: list, save: bool, path: str, naming: str)
+    > * prompts: list of prompts
+    > save: If true, images will save to a jpg file.
+    > path: To save the images to a folder.
+    > naming ('counter', 'prompt'): Sets the image's filename to include either the counter or prompt.

+ pollinations.ai.ImageObject.save(save_file: str) >> Save the image to a file.
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
