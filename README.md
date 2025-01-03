<div id="header">
  <img src="https://i.ibb.co/p049Y5S/86964862.png" width="50"/>   <img src="https://i.ibb.co/r6JZ336/sketch1700556567238.png" width="250">
</div>

# [pollinations.ai - Image Generation](https://pypi.org/project/pollinations.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/toolkitr/tkr/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20-blue)](https://www.python.org/downloads/)

```
pollinations.ai: (https://pollinations.ai/)

Work with the best generative models from Pollinations using this python wrapper.
```

## Installing
```shell
pip install -U pollinations
pip install -U pollinations.ai

# Linux/macOS
python3 -m pip install -U pollinations
python3 -m pip install -U pollinations.ai

# Windows
py -3 -m pip install -U pollinations
py -3 -m pip install -U pollinations.ai
```

## Image Generation
```python
import pollinations

image_model = pollinations.Image(
    model=pollinations.Image.flux(),
    seed="random",
    width=1024,
    height=1024,
    enhance=True,
    nologo=True,
    private=True
)  # or pollinations.Image()

image_model.generate(
    prompt="A magical voodoo wizard in space, surounded by flowers.",
    negative="Realistic, depth of field, blurry",
    save=True,
    file="my_file.png"
)

image = image_model.generate(
    prompt="A magical voodoo wizard in space, surounded by flowers.",
    negative="Realistic, depth of field, blurry",
    save=False,
    file="my_file.png"
)

print(image.model, image.prompt)

print(image_model.models())  # Tuple of models
print(image_model.flux())  # String
print(image_model.flux().info())  # Dict
```
## Text Generation
```python
import pollinations

text_model = pollinations.Text(
    model=pollinations.Text.openai(),
    contextual=True,
    seed="random",
    system="You are a helpful AI Assistant... ",
    limit=20
)  # or pollinations.Text()

text_model.generate(
    prompt="Hello", 
    display=True
)

response = text_model.generate(
    prompt="Hey",
    display=False
)

print(response.text, response.model, response.prompt)

text_model.image(
    file="image.png"
)

text_model.generate(
    prompt="What do you see in this image?",
    display=True
)

print(text_model.models())  # Tuple of models
print(text_model.openai())  # String
print(text_model.openai().info())  # Dict
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
