<div id="header">
  <img src="https://i.ibb.co/p049Y5S/86964862.png" width="50"/>   <img src="https://i.ibb.co/r6JZ336/sketch1700556567238.png" width="250">
</div>

# [pollinations.ai - Free AI Text & Image Generation](https://pypi.org/project/pollinations.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/pollinations-ai/pollinations.ai/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/badge/python-3%20%7C%203.10--3.13-blue)](https://www.python.org/downloads/)


```
pollinations.ai: (https://pollinations.ai/)

Work with the best generative models from Pollinations using this Python SDK.
```
# FIX 2.3.3
```diff
+ Updated license & badge markdown
```
# UPDATE 2.3.2
```diff
+ Async class
```
```python
import asyncio
import pollinations

async def async_test():
    text_model = pollinations.Async.Text()  # Has ALL features and functionality as normal Text class
    await text_model(
        prompt="Hello"
    )
    
    print(text_model.response)
    
    image_model = pollinations.Async.Image()  # Has ALL features and functionality as normal Image class
    await image_model(
        prompt="A black cat."
    )
    
    await image_model.save(
        file="pollinations-image.png"
    )
    
asyncio.run(async_test())
```
# FIX 2.3.1
```diff
+ Updated classifiers
+ Updated keywords
+ Docstrings
```
# UPDATE 2.3
```diff
+ Updated Text class
+ Updated Image class
```
```python
"""
class Text(
    model: str = "openai",
    system: str = "",
    contextual: bool = False,
    messages: list = [],
    seed: int = "random",
    jsonMode: bool = False,
    ...
)
"""

model = pollinations.Text(
    model=pollinations.Text.openai(),
    system="You are a helpful assistant...",
    contextual=True,
    messages=[
        pollinations.Text.Message(
            role="user",
            content="What is the capital of France?"
        ),
        pollinations.Text.Message(
            role="assistant",
            content="The capital of France is Paris."
        )
    ],
    seed=42,
    jsonMode=True
)

"""
(method) def info(...) -> dict
"""

print(pollinations.Text.openai.info())

"""
(method) def image(
    file: str | list,
    ...
) -> Text
"""

model.image("my_file.png")
print("\n", model(
    prompt="What do you see in this image?"
).response)

"""
(method) def __call__(
    prompt: str = None,
    display: bool = False,
    ...,
    encode: bool = False
) -> Text
"""

response = model(encode=True)  # use proper encoding
print("\n", response.response, response.time, response.request)  # The capital of France is Paris., ..., Text.Request(...)

print("\n", model(
    prompt="Hello.",
    display=True,  # simulate typing
    encode=False
).response)

# ---------------------------------------------- #

"""
class Request(
    model: str,
    prompt: str,
    ...,
    system: str = "",
    contextual: bool = False,
    messages: List[dict] = None,
    seed: str | int = "random",
    jsonMode: bool = False
)
"""

"""
class Message(
    role: str,
    content: str,
    images: dict | list = None
)

(method) def image(
    file: str,
    ...
) -> dict
"""

request = pollinations.Text.Request(
    model=pollinations.Text.openai(),
    prompt="Hello. Whats in this image?",
    system="You are a helpful assistant...",
    contextual=True,
    messages=[
        pollinations.Text.Message(
            role="user",
            content="What is the capital of France?"
        ),
        pollinations.Text.Message(
            role="assistant",
            content="The capital of France is Paris."
        )
    ],
    images=[
        pollinations.Text.Message.image("my_file.png"),
        pollinations.Text.Message.image("my_file2.png")    
    ], 
    seed=42,
    jsonMode=True
)

print("\n", request(
    encode=True
))
```
```python
"""
class Image(
    model: str = "flux",
    seed: str | int = "random",
    width: int = 1024,
    height: int = 1024,
    enhance: bool = False,
    nologo: bool = False,
    private: bool = False,
    safe: bool = False
)
"""

model = pollinations.Image(
    model=pollinations.Image.flux(),
    seed="random",
    width=1024,
    height=1024,
    enhance=False,
    nologo=False,
    private=False,
    safe=False
)

"""
(method) def info(...) -> dict
"""

print(pollinations.Image.flux.info())

"""
(method) def __call__(
    prompt: str,
    *args: Any
) -> Image
"""

image = model(
    prompt="A cat with flowers around it."
)

print(image.prompt, image.file)

"""
(method) def save(file: str = "pollinations-image.png") -> Image
"""

image.save(
    file="pollinations-image.png"
)

# ---------------------------------------------- #

"""
class Request(
    model: str = "flux",
    prompt: str = "",
    seed: str | int = "random",
    width: int = 1024,
    height: int = 1024,
    enhance: bool = False,
    nologo: bool = False,
    private: bool = False,
    safe: bool = False
)
"""

request = pollinations.Image.Request(
    model=pollinations.Image.flux(),
    prompt="A cat with flowers around it.",
    seed="random",
    width=1024,
    height=1024,
    enhance=False,
    nologo=False,
    private=False,
    safe=False
)

print(request)

request()

print(request.prompt, request.response)
```
# UPDATE 2.2
```diff
+ Text class
+ Image class
- TextObject class
- ImageObject class
- TextModel class
- ImageModel class
```
```python
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
```python
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
    safe=False,  # Strict NSFW check
    save=True,
    file="my_file.png"
)

image = image_model.generate(
    prompt="A magical voodoo wizard in space, surounded by flowers.",
    safe=False,  # Strict NSFW check
    save=False,
    file="my_file.png"
)

print(image.model, image.prompt)

print(image_model.models())  # Tuple of models
print(image_model.flux())  # String
print(image_model.flux().info())  # Dict
```
# UPDATE 2.1
```diff
+ Added image method to TextModel object for vision (Works with some models)

+ Added qwen-coder model
+ Added evil model
- Removed MultiModel
- Removed SmartModel
- Removed Aspect constraints on images
```
```python
text_model.image(
    file="my_file.png"
)
text_model.generate(
    prompt="Describe that file.",
    display=True
)
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
