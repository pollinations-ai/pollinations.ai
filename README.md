<div id="header">
  <img src="https://i.ibb.co/WpWqrTN3/pollinations-logo-icon-black-png.png" width="50"/>   <img src="https://i.ibb.co/r6JZ336/sketch1700556567238.png" width="250">
</div>

# [pollinations.ai -  Free AI Image, Text, and Audio Generation](https://pypi.org/project/pollinations)
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

# Usage

## Image Generation
<details>
<summary>View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Image,
    model: ImageModel | None = "flux",
    width: Width | None = 1024,
    height: Height | None = 1024,
    seed: Seed | None = "random",
    nologo: NoLogo | None = False,
    private: Private | None = False,
    enhance: Enhance | None = False,
    safe: Safe | None = False,
    referrer: Referrer | None = "pollinations.py",
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Image()

"""
(method) def __call__(
    self: Self@Image,
    prompt: Prompt,
    negative: Negative | None = "",
    *args: Args,
    file: Filename | None = "pollinations-image.jpeg",
    save: Save = False,
    *kwargs: Kwargs
) -> PILImage
"""

image = model("A dog and cat.")
image.save("my_image.jpeg")
# Alternatively:
# image = model.Generate("A dog and cat.", file="my_image.jpeg", save=True)
```
</details>

<details>
<summary>(Async) View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Image,
    model: ImageModel | None = "flux",
    width: Width | None = 1024,
    height: Height | None = 1024,
    seed: Seed | None = "random",
    nologo: NoLogo | None = False,
    private: Private | None = False,
    enhance: Enhance | None = False,
    safe: Safe | None = False,
    referrer: Referrer | None = "pollinations.py",
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Image()

"""
(method) async def Async(
    self: Self@Image,
    prompt: Prompt,
    negative: Negative | None = "",
    *args: Args,
    file: Filename | None = "pollinations-image.jpeg",
    save: Save = False,
    *kwargs: Kwargs
) -> PILImage
"""

image = await model.Async("A dog and cat.")
image.save("my_image.jpeg")
# Alternatively:
# image = await model.Async("A dog and cat.", file="my_image.jpeg", save=True)
```
</details>

## Text Generation
<details>
<summary>View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Text,
    model: Model | None = "openai",
    system: System | None = "You are a helpful AI assistant.",
    contextual: Contextual | None = False,
    messages: Messages | None = [],
    private: Private | None = False,
    seed: Seed | None = "random",
    reasoning_effort: ReasoningEffort | None = "medium",
    tools: Tools | None = [],
    tool_choices: ToolChoice | None = [],
    voice: Voice | None = None,
    json_mode: JsonMode | None = False,
    referrer: Referrer | None = "pollinations.py",
    openai_endpoint: UseOpenAIEndpoint | None = False,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Text()

"""
(method) def __call__(
    self: Self@Text,
    prompt: Prompt | None = None,
    *any_kwargs_will_be_passed_in_request: Args,
    stream: Stream | None = False,
    **kwargs: Kwargs
) -> Output
"""

print(model("Hello, what is 1 + 1?"))
# Alternatively:
# print(model.Generate("Hello, what is 1 + 1?"))


# Streaming
for token in model("Hello, what is 1 + 1?", stream=True):
    print(token, end="", flush=True)
    
# Alternatively:
# for token in model.Generate("Hello, what is 1 + 1?", stream=True):
#     print(token, end="", flush=True)
```
</details>

<details>
<summary>(Async) View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Text,
    model: Model | None = "openai",
    system: System | None = "You are a helpful AI assistant.",
    contextual: Contextual | None = False,
    messages: Messages | None = [],
    private: Private | None = False,
    seed: Seed | None = "random",
    reasoning_effort: ReasoningEffort | None = "medium",
    tools: Tools | None = [],
    tool_choices: ToolChoice | None = [],
    voice: Voice | None = None,
    json_mode: JsonMode | None = False,
    referrer: Referrer | None = "pollinations.py",
    openai_endpoint: UseOpenAIEndpoint | None = False,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Text()

"""
(method) async def Async(
    self: Self@Text,
    prompt: Prompt | None = None,
    *any_kwargs_will_be_passed_in_request: Args,
    stream: Stream | None = False,
    **kwargs: Kwargs
) -> Output
"""

print(await model.Async("Hello, what is 1 + 1?"))

# Streaming
async for token in await model.Async("Hello, what is 1 + 1?", stream=True):
    print(token, end="", flush=True)
```
</details>

## Audio Transcription
<details>
<summary>View Code Examples</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Text,
    model: Model | None = "openai",
    system: System | None = "You are a helpful AI assistant.",
    contextual: Contextual | None = False,
    messages: Messages | None = [],
    private: Private | None = False,
    seed: Seed | None = "random",
    reasoning_effort: ReasoningEffort | None = "medium",
    tools: Tools | None = [],
    tool_choices: ToolChoice | None = [],
    voice: Voice | None = None,
    json_mode: JsonMode | None = False,
    referrer: Referrer | None = "pollinations.py",
    openai_endpoint: UseOpenAIEndpoint | None = False,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Text()

"""
(method) def Transcribe(
    self: Self@Text,
    file: Filename,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs
) -> Output
"""

print(model.Transcribe("my_audio.mp3"))
```
</details>
<details>
<summary>(Async) View Code Examples</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Text,
    model: Model | None = "openai",
    system: System | None = "You are a helpful AI assistant.",
    contextual: Contextual | None = False,
    messages: Messages | None = [],
    private: Private | None = False,
    seed: Seed | None = "random",
    reasoning_effort: ReasoningEffort | None = "medium",
    tools: Tools | None = [],
    tool_choices: ToolChoice | None = [],
    voice: Voice | None = None,
    json_mode: JsonMode | None = False,
    referrer: Referrer | None = "pollinations.py",
    openai_endpoint: UseOpenAIEndpoint | None = False,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs,
) -> None
"""

model = pollinations.Text()

"""
(method) def Transcribe(
    self: Self@Text,
    file: Filename,
    *any_kwargs_will_be_passed_in_request: Args,
    **kwargs: Kwargs
) -> Output
"""

print(await model.TranscribeAsync("my_audio.mp3"))
```
</details>

## Audio Generation
Coming soon

## Feed Reading
<details>
<summary>View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Feed,
    type: FeedType = "image",
    max_data: MaxData | None = None,
    *args: Args, 
    **kwargs: Kwargs
) -> None
"""

feed = pollinations.Feed()
# feed = pollinations.Feed("text", 10)  # Optionally specify type and amount

"""
(method) def __call__(
    self: Self@Feed,
    *args: Args, 
    **kwargs: Kwargs
) -> Iterator[Data]
"""

for item in feed():
    print(len(feed.data), item.data)

# Alternatively:
# for item in feed.Get():
#     print(len(feed.data), item.data)
```
</details>
<details>
<summary>(Async) View Code Example</summary>

```python
import pollinations

"""
(method) def __init__(
    self: Self@Feed,
    type: FeedType = "image",
    max_data: MaxData | None = None,
    *args: Args, 
    **kwargs: Kwargs
) -> None
"""

feed = pollinations.Feed()
# feed = pollinations.Feed("text", 10)  # Optionally specify type and amount

"""
(method) async def Async(
    self: Self@Feed,
    *args: Args, 
    **kwargs: Kwargs
) -> AsyncIterator[Data]
"""

async for item in feed.Async():
    print(len(feed.data), item.data)
```

</details>

<br>

# Links
- [SDK-Repository](https://github.com/pollinations-ai/pollinations.ai)
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
