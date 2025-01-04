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
    enhance=False,
    nologo=True,
    private=True,
    safe=False
)  # or pollinations.Image() to use defaults

image = image_model(
    prompt="A cat with flowers around it."
)

print(image.prompt, image.response)

image.save(
    file="pollinations-image.png"
)

print(pollinations.Image.models())
print(pollinations.Image.flux())
print(pollinations.Image.flux.info())
```
### Async Image Generation
```python
image_model = pollinations.Async.Image()  # Has ALL features and functionality of normal Image class

image = await image_model(
    prompt="A cat with flowers around it."
)
```
## Text Generation
```python
import pollinations

text_model = pollinations.Text(
    model=pollinations.Text.openai(),
    system="You are a helpful assistant.",
    contextual=True,
    messages=[  # or [] or None
        pollinations.Text.Message(
            role="user",
            content="What is the capital of France?"
        ),
        pollinations.Text.Message(
            role="assistant",
            content="The capital of France is Paris."
        )
    ],
    seed="random",
    jsonMode=False
)

response = text_model(
    prompt="Hello.",
    display=True,  # Simulate typing,
    encode=True  # Use proper encoding
)

print(response.prompt, response.response)

print(pollinations.Text.models())
print(pollinations.Text.openai())
print(pollinations.Text.openai.info())
```
### Async Text Generation
```python
text_model = pollinations.Async.Text()  # Has ALL features and functionality of normal Text class

response = await text_model(
    prompt="Hello."
)
```
## Image Request Building
```python
import pollinations

image_request = pollinations.Image.Request(
    model=pollinations.Image.flux(),
    prompt="A cat with flowers around it.",
    seed="random",
    width=1024,
    height=1024,
    enhance=False,
    nologo=True,
    private=True,
    safe=False
)

image = image_request()

print(image.model, image.prompt, image.response)
```

## Text Request Building
```python
import pollinations

text_request = pollinations.Text.Request(
    model=pollinations.Text.openai(),
    prompt="Hello, how are you?",
    system="You are a helpful assistant.",
    contextual=True,
    messages=[  # or [] or None
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
    seed="random",
    jsonMode=False
)

response = text_request(
    encode=True  # Use proper encoding
)
print(response)
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Repository](https://github.com/pollinations-ai/pollinations.ai)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
