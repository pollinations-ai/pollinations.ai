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

# CHANGELOG V0.2.4
```diff
+ Added the model, width, height, and seed params to ai.Image.generate()

* prompt
(Optional):
  model='turbo'
  width=1024
  height=1024
  seed='random'
```
### NEW
```python
import pollinations.ai as ai

model: ai.Image = ai.Image()
image: ai.ImageObject = model.generate(
      prompt='lion feasting on prey',
      model='pixart',
      width=1024,
      height=1024,
      seed=711144046
).save()
print(image.prompt, image.url)

# >>> lion feasting on prey https://image.pollinations.ai/prompt/lion%20feasting%20on%20prey?model=pixart&width=1024&height=1024&seed=711144046

```

# CHANGELOG V0.2.3

## Installing
```shell
# Linux/macOS
python3 -m pip install -U pollinations.ai

# Windows
py -3 -m pip install -U pollinations.ai
```

V0.2.1 UPDATES:
```diff
+ Complete code refactor for pollinations.__init__, 
+      pollinations.abc, 
+      pollinations.ai, 
+      pollinations.ext, 
+      and added pollinations.types
```

```python
import pollinations.ai as ai

model: ai.Text = ai.Text()

response: str = model.chat('What is the meaning of life?')
```

## Added
```python
pollinations.types

pollinations.types.ImageModel
pollinations.types.ImageObject

pollinations.types.TextModel
pollinations.types.TextObject
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
