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

## Installing
```shell
# Linux/macOS
python3 -m pip install -U pollinations.ai

# Windows
py -3 -m pip install -U pollinations.ai
```

# Simple Examples
```python
import pollinations.ai as ai

prompt: str = 'A cat with a top hat and a mustache.'
prompt_sample: str = ai.sample()

image_generator: ai.Image = ai.Image(save_file='pollinations.ai.jpg') # OPTIONAL: takes save_file parameter
image = image_generator.generate(prompt)
image.save() # OPTIONAL: takes save_file parameter
```
Chatting with text generative ai model:
```python
import pollinations.ai as ai

model: ai.Text = ai.Text()

response: str = model.chat(prompt='What is the meaning of life?')
```

Setting model filter:
```python
import pollinations.ai as ai

image_generator: ai.Image = ai.Image()
image_generator.set_filter(ai.BANNED_WORDS)

# If any word from a prompt is in the filter it will return an exception.
```
Batch sample and generation:
```python
import pollinations.ai as ai

batch: list = ai.sample_batch(size=5)
image_generator: ai.Image = ai.Image()
image_generator.generate_batch(prompts=batch, save=True) # OPTIONAL: path  # OPTIONAL: naming = 'counter' | naming = 'prompt'

# image_generator.generate_batch(prompts=batch, save=True, path='somefolder', naming='prompt')
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
