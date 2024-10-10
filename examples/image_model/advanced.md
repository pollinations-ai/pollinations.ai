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
# ImageObject(...)
```

<div id="header">
  <img src="https://camo.githubusercontent.com/3218ab6f2a6bc6b07177e3083d886fffa1ad2591fd0bf981241de1794afdebee/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f412532306d61676963616c253230766f6f646f6f25323077697a617264253230696e25323073706163652c2532307375726f756e6465642532306279253230666c6f776572732e3f6e656761746976653d5265616c69737469632c25323064657074682532306f662532306669656c642c253230626c7572727926736565643d353031323038333133312677696474683d31303234266865696768743d31303234266e6f6c6f676f3d46616c736526707269766174653d54727565266d6f64656c3d666c75782d616e696d6526656e68616e63653d54727565" width=500/>
</div>

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
