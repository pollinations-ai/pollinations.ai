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

# UPDATE 2.0.10
```diff
+ Slight tweaks to models
+ Fixed charset issue
+ Added .save() to ImageObject + updated params
+ Updated model list + key fix
```
```python
result = chardet.detect(request.content)
encoding = result['encoding']
content = request.content.decode(encoding)
```

# REWRITE 2.0.0
```diff
- All previous code
+ All new code

+ ImageModel
+ TextModel
+ MultiModel
+ SmartModel
```
### Examples
## Image Model
```python
import pollinations

image_model: pollinations.ImageModel = pollinations.image(
    model = pollinations.image_default,
    seed = 0,
    width = 1024,
    height = 1024,
    enhance = False,
    nologo = False,
    private = False,
)

image_model.generate(
    prompt = "A black cat in a cyberpunk city.",
    negative = "Anime, cartoony, childish.",
    save = True,
    file = "image-output.png",
)
```
## Text Model
```python
import pollinations

text_model: pollinations.TextModel = pollinations.text(
    frequency_penalty = 0,
    presence_penalty = 0,
    temperature = 0.5,
    top_p = 1,
    model = pollinations.text_default,
    stream = True,
    contextual = True, # True: Holds conversation context up to 10. False: Has no conversation context
    system = "You are a polite AI Assistant named Pollinations! Use emojis and markdown as you wish."
)

text_model.generate(
    prompt="What is 1+1?",
    display=True
)
text_model.generate(
    prompt="Now add 10 to that.",
    display=True
)
```
## Multi Model (Image & Text)
```python
import pollinations

multi_model: pollinations.MultiModel = pollinations.multi(
    system = "You are a polite AI Assistant named Pollinations! Use emojis and markdown as you wish.",
    default = None, # None: AI will infer what model to use. Example: pollinations.turbo: Will default image model to turbo
    text_model = pollinations.text_default, # Safety fail measure incase of model errors in pollinations api.
    image_model = pollinations.image_default, # Safety fail measure incase of model errors in pollinations api.
)

multi_model.generate(
    "Hi",
    display=True,
    provide_details=False # Provides the details and objects of each generation
)
multi_model.generate(
    "Make an image of a black dog in a cyberpunk city.",
    display=True,
    provide_details=False
)
multi_model.generate(
    "Thanks.",
    display=True,
    provide_details=False
)
```
## Smart Model (MultiModel up-to-date with time, dates, weather, and search) (Primitive Testing)
```python
import pollinations

# Searching will not work unless you provide a serpapi api-key like this:
pollinations.keys(serpapi="your-key")

smart_model: pollinations.SmartModel = pollinations.smart(
    system="You are a helpful and friendly AI assistant. Use emojis and markdown as you like.",
    text_model=pollinations.mistral_large,      # Optional
    # image_model=pollinations.flux_anime       # Optional : If not directly chosen, the best fit model according to prompt will be chosen.
)

smart_model.generate(
    prompt="Hi.",
    display=True,
    provide_details=False    # Provide extra details of each generation.
)
smart_model.generate(
    prompt="What is the weather in london like?",
    display=True,
    provide_details=False
)
smart_model.generate(
    prompt="What's the latest news there as well?",
    display=True,
    provide_details=False
)
smart_model.generate(
    prompt="What time is it in New York City?",
    display=True,
    provide_details=False
)
smart_model.generate(
    prompt="Make an image of that at night, include city lights.",
    display=True,
    provide_details=False
)
smart_model.generate(
    prompt="Thanks.",
    display=True,
    provide_details=False
)
```

# Links
- [Pollinations.ai](https://pollinations.ai/)
- [Discord](https://discord.gg/8HqSRhJVxn)
- [Github](https://github.com/pollinations)
- [Youtube](https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug)
- [Instagram](https://instagram.com/pollinations_ai)
- [Twitter (X)](https://twitter.com/pollinations_ai)
