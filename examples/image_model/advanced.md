```python
import pollinations

image_model: pollinations.ImageModel = pollinations.image(
    model=pollinations.flux_anime,
    seed="random", # A random seed for the image OR put a number. Example: 42
    width=1024,
    height=1024,
    enhance=True, # Use AI to enhance the prompt further.
    nologo=False, # Remove watermark,
    private=True # Will not show up on pollinations.ai public feed
)

image_model.generate(
    prompt="A magical voodoo wizard in space, surounded by flowers.",
    negative="Realistic, depth of field, blurry",
    save=True,
    file="my_file.png"
)
```



```
Pollinations will figure out the closest aspect ratio to whatever you put in, limiting it to one of these options.
Aspect Ratios: {'1:1': (1024, 1024), '3:4': (768, 1024), '16:9': (1024, 576)}

Examples:

width=1024,
height=1024

width=1,
height=1

--------------

width=768,
height=1024

width=3,
height=4

--------------

width=1024,
height=576

width=16,
height=9
```
