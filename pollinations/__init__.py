"""
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

## Audio Generation
```python
# Coming in a future update
```
"""

# MIT License

# Copyright (c) 2025 pollinations

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pollinations.core.text import Text  # noqa: F401
from pollinations.core.image import Image  # noqa: F401

from pollinations.models import Model, text_models, image_models

__version__ = "3.5.1"
__license__ = "MIT"
__description__ = (
    "Work with the best generative AI from Pollinations using this Python SDK. 🐝"
)
__all__ = ["Text", "Image", "Model", "text_models", "image_models", "__version__", "__license__", "__description__"]
