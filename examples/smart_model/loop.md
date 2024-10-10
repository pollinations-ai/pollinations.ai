```python
import pollinations

# Required:
pollinations.keys(serpapi="your-api-key") # https://serpapi.com/

smart_model: pollinations.SmartModel = pollinations.smart(
    system="You are a friendly AI Assistant. Use emojis and markdown as you like.",
    text_model=pollinations.text_default,
    image_model=pollinations.image_default
)

while True:
    prompt: str = input("User:\n> "); print("\nPollinations:\n> ", end="")
    smart_model.generate(
        prompt=prompt,
        display=True,
        provide_details=True
    ); print()
```

```
User:
> Hello.

Pollinations:
> Hey there! 😊 How's it going?

User:
> What time is it in Toronto? 

Pollinations:
> It's 04:03:07 PM in Toronto right now! 🕓

User:
> Can you make an image there?

Pollinations:
> Sure! Generating your image related to the prompt! 🖼 

User:
> Thanks.

Pollinations:
> Of course! 😊
```
<div id="header">
  <img src="https://camo.githubusercontent.com/8a8d814521986095e50db80507a69b84e10fff14fb0f18e63b21ac3ab48313d9/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f437265617465253230612532307374756e6e696e67253230696d616765253230646570696374696e672532306125323076696272616e742532307363656e65253230696e253230546f726f6e746f2e3f6e656761746976653d26736565643d383435353031373533352677696474683d31303234266865696768743d31303234266e6f6c6f676f3d5472756526707269766174653d54727565266d6f64656c3d666c757826656e68616e63653d54727565" width=500/>
</div>
