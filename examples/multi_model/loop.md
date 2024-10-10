```python
import pollinations

multi_model: pollinations.MultiModel = pollinations.multi(
    system="You are a friendly AI Assistant. Use emojis and markdown as you like.",
    default=pollinations.flux_3D, 
    text_model=pollinations.text_default,
    image_model=pollinations.image_default
)

while True:
    prompt: str = input("User:\n> "); print("\nPollinations:\n> ", end="")
    multi_model.generate(
        prompt=prompt,
        display=True,
        provide_details=True
    ); print()
```

```
User:
> Hi.

Pollinations:
> Hello! 😊 How's your day going?

User:
> Can you make me an image of mario on a dinosaur?

Pollinations:
> Sure! Generating your image of Mario on a dinosaur! 🌟🦖
```
<div id="header">
  <img src="https://camo.githubusercontent.com/82e0c0c834342a8c01596816930208c8603d4101473b1b296b5df947ad4cfc1b/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f43726561746520616e20696d616765206f66204d6172696f206a6f7966756c6c7920726964696e67206120636f6c6f7266756c2064696e6f73617572207468726f75676820612076696272616e74206c616e6473636170652e3f6e656761746976653d26736565643d373930393334343038322677696474683d31303234266865696768743d31303234266e6f6c6f676f3d5472756526707269766174653d54727565266d6f64656c3d666c75782d336426656e68616e63653d54727565" width=500/>
</div>
