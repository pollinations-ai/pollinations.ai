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

while True:
    prompt: str = input("Prompt> ")
    negative: str = input("Negative> ")
    image_model.generate(
        prompt=prompt,
        negative=negative,
        save=True,
        file="my_file.png"
    )
    print("---------------")
```

## Example
```
Prompt> Black cat in a cyberpunk city.    
Negative> Realistic, blurry, depth of field
---------------
```

<div id="header">
  <img src="https://camo.githubusercontent.com/b39e4d215c033d08d716bf5b0183da2ad5458b5c32b60e8cd0e1f6f1cf5554b8/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f426c61636b253230636174253230696e25323061253230637962657270756e6b253230636974792e3f6e656761746976653d5265616c69737469632c253230626c757272792c25323064657074682532306f662532306669656c6426736565643d393133323035393531362677696474683d31303234266865696768743d31303234266e6f6c6f676f3d46616c736526707269766174653d54727565266d6f64656c3d666c75782d616e696d6526656e68616e63653d54727565" width=500/>
</div>

