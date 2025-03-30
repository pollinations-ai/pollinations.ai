```python
import pollinations

image_model = pollinations.Image(
    model="flux",
    seed="random",  # A random seed for the image OR put a number. Example: 42
    width=512,
    height=512,
    enhance=False,  # Use AI to enhance the prompt further.
    nologo=True,  # Remove watermark,
    private=True,  # Will not show up on pollinations.ai public feed
    safe=False, # Strict NSFW check
    referrer="pollinations.py"
)

while True:
    prompt: str = input("Prompt> ")
    image_model(
        prompt=prompt,
    ).save(
        file="pollinations-image.png"
    )
    print("---------------")
```

## Example
```
Prompt> Moon colony
---------------
```

<div id="header">
  <img src="https://i.ibb.co/Msrs4Hf/image.png" width=500/>
</div>

