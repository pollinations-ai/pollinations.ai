```python
import pollinations

# Required:
pollinations.keys(serpapi="your-api-key") # https://serpapi.com/

smart_model: pollinations.SmartModel = pollinations.smart(
    system="You are a friendly AI Assistant. Use emojis and markdown as you like.",
    text_model=pollinations.mistral_large,
    image_model=pollinations.image_default
)

smart_model.generate(
    prompt="Hi",
    display=True,
    provide_details=True
)
smart_model.generate(
    prompt="What time is it in London?",
    display=True,
    provide_details=True
)
smart_model.generate(
    prompt="What is the weather like there?",
    display=True,
    provide_details=True
)
smart_model.generate(
    prompt="Whats the latest news from BBC?",
    display=True,
    provide_details=True
)
smart_model.generate(
    prompt="Can you make an image of earth viewed from the moon.",
    display=True,
    provide_details=True
)
```

```
Hello! 😊 How's your day going?
It's currently 8:58 PM in London. 🕛✨
The weather in London is 25.8°C with some nice conditions. ☀️🌤 ️ Enjoy the warmth!
Here are a couple of the latest headlines from BBC News:

1. **[Home - BBC News](https://www.bbc.com/news)**: Up-to-the-minute news and breaking stories.
   
2. **[World | Latest News & Updates](https://www.bbc.com/news/world)**: Four killed by tornadoes in Florida, with warnings of more Hurricane Milton flooding. 🌪 

Feel free to check the links for more details! 📰
Sure! Generating your image of Earth viewed from the Moon! 🌍🌕
```
<div id="header">
  <img src="https://camo.githubusercontent.com/d1d58fac2cdf006cf513d66c91d5e965bc0b97bb7e1e83d07987059691678714/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f437265617465253230612532307374756e6e696e67253230696d6167652532306f66253230456172746825323061732532307365656e25323066726f6d2532307468652532304d6f6f6e2f2773253230737572666163652c253230636170747572696e67253230746865253230766173746e6573732532306f6625323073706163652e3f6e656761746976653d26736565643d353030333532373633342677696474683d31303234266865696768743d31303234266e6f6c6f676f3d5472756526707269766174653d54727565266d6f64656c3d666c757826656e68616e63653d54727565" width=500/>
</div>
