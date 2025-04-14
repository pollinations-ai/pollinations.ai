<div id="header">
  <img src="https://i.ibb.co/p049Y5S/86964862.png" width="50"/>   <img src="https://i.ibb.co/r6JZ336/sketch1700556567238.png" width="250">
</div>

# [pollinations.ai - Free AI Text & Image Generation](https://pypi.org/project/pollinations)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/pollinations-ai/pollinations.ai/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/badge/python-3%20%7C%203.10--3.13-blue)](https://www.python.org/downloads/)

```
pollinations.ai: (https://pollinations.ai/)

Work with the best generative AI from Pollinations using this Python SDK. 🐝
```

## Installing
```shell
pip install pollinations
pip install pollinations.ai

# Linux/macOS
python3 -m pip install pollinations
python3 -m pip install pollinations.ai

# Windows
py -3 -m pip install pollinations
py -3 -m pip install pollinations.ai
```

## Image Generation
```python
model = pollinations.Image(  # Optional Arguments
    model="flux",
    seed="random",
    file="pollinations-image.png",
    width=1024,
    height=1024,
    nologo=False,
    private=False,
    enhance=False,
    safe=False,
    referrer="pollinations.py",
)

print(model.models())

image = model("A dog and cat.")  # Returns pillow Image instance

image.save("image.png")  
# (or) 
# (optional) model.file="image.png"
image = model("A dog and cat.", save=True)
```

## Async Image Generation
```python
async def async_example():
    image = await model.Async("A horse and pig.")
    # image = await model.Async("A horse and pig.", save=True)

    image.save("a_image.png")
    print(image)
    print(model)
```

## Text Generation
```python
model = pollinations.Text(  # Optional Arguments
    model="openai",
    system="You are a helpful assistant.",
    contextual=True,
    messages=[],
    private=False,
    seed="random",
    reasoning_effort="medium",
    tools=[],
    tool_choices=[],
    voice=None,
    json_mode=False,
    referrer="pollinations.py",
)

print(model.models())

print(model("Hello world"))

model.image("image.png")  # model.image(["image1.png", "image2.png", ...])
print(model("What do you see in that image?"))


# Stream Request
for token in model("Explain AI at a low level.", stream=True):
    print(token, end="", flush=True)
```

## Async Text Generation
```python
async def async_example():
    image = await model.Async("A horse and pig.")
    # image = await model.Async("A horse and pig.", save=True)

    image.save("a_image.png")
    print(image)
    print(model)
```

## Audio Transcription
```python
model = pollinations.Text()

print(model.Transcribe("test.mp3"))
```

## Async Audio Transcription
```python
model = pollinations.Text()

async def async_example():
    print(await model.TranscribeAsync("my_audio.mp3"))
```

## Audio Generation
```python
# Coming in a future update
```

## Async Audio Generation
```python
# Coming in a future update
```

# Links
- [SDK-Repository](https://github.com/pollinations-ai/pollinations.ai)
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
