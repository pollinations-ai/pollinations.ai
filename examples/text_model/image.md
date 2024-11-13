```python
import pollinations

text_model: pollinations.TextModel = pollinations.text(
    frequency_penalty=0,
    presence_penalty=0,
    temperature=0.5,
    top_p=1,
    model=pollinations.text_default,
    stream=True,
    contextual=True, # Hold conversation
    system="You are a helpful AI Assistant. Use emojis and markdown when you like."
)

text_model.generate(
    prompt="Hello", 
    display=True # Simulates typing text.
)
# TextObject(...)
text_model.generate(
    prompt="What was my first message?", 
    display=True # Simulates typing text.
)
# TextObject(...)
text_model.image(
    file="my_file.png"
)
# bool
text_model.generate(
    prompt="Describe that image please.", 
    display=True # Simulates typing text.
)
# TextObject(...)
```

<div id="header">
  <img src="https://media.discordapp.net/attachments/889573359111774329/1306074575347515514/image.png?ex=6735583c&is=673406bc&hm=8fd16f30b991a091dc8fb4793d02f4ff041cdd05d957f7d49ea64b2e7caa9590&=&format=webp&quality=lossless&width=503&height=503" width=500/>
</div>

```
Hello! 🌟 How can I assist you today?
Your first message was: "Hello" 😊. How can I help you further?
The file depicts a photo of two individuals posing together in a dimly lit environment, possibly at a social gathering or event. The background contains some lights, suggesting a lively atmosphere. One person is wearing a dark jacket, while the other has long hair and is dressed in a black top. The overall mood of the image appears to be casual and cheerful. 🎉😊
```
