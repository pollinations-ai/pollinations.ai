```python
import pollinations

image_model = pollinations.Image(
    model=pollinations.Image.flux().name,
    seed="random", # A random seed for the image OR put a number. Example: 42
    width=1024,
    height=1024,
    enhance=True, # Use AI to enhance the prompt further.
    nologo=False, # Remove watermark,
    private=True # Will not show up on pollinations.ai public feed
)

while True:
    prompt: str = input("Prompt> ")
    image_model.generate(
        prompt=prompt,
        safe=False,  # Strict NSFW check
        save=True,
        file="my_file.png"
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

