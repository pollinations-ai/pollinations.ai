```python
import pollinations

multi_model: pollinations.MultiModel = pollinations.multi(
    system="You are a friendly AI Assistant. Use emojis and markdown as you like.",
    default=None,  # Use a default image model for all cases.
    text_model=pollinations.mistral_large,  # Use a default text model for all cases.
    image_model=pollinations.flux_anime     # Use a default image model incase of default model or model guess failure.
)

multi_model.generate(
    prompt="Hi",
    display=True,
    provide_details=True # Extra prompt details
)
multi_model.generate(
    prompt="Can you make me an image of mario as an astronaut on the moon. Cartoony",
    display=True,
    provide_details=True
)
```

```
Hello! 😊 How can I help you today?
Sure thing! 🚀🌙 Creating your Mario astronaut image!
```
<div id="header">
  <img src="https://camo.githubusercontent.com/31d924490aa42f63649637a0b8ca72975833a6561abe3733dcbfbf565f7b9858/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f4d6172696f253230617325323061253230636865657266756c253230617374726f6e6175742532306f6e2532307468652532306d6f6f6e2c253230636172746f6f6e2532307374796c652532302546302539462539412538302546302539462538432539392546302539462538442538343f6e656761746976653d26736565643d393130373738393931352677696474683d31303234266865696768743d31303234266e6f6c6f676f3d5472756526707269766174653d54727565266d6f64656c3d666c75782d616e696d6526656e68616e63653d54727565" width=500/>
</div>
