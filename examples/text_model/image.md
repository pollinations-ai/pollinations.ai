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
  <img src="https://camo.githubusercontent.com/88a599c4b118818631d62917da8c16cb17f1d59074dab395827104ca64272baa/68747470733a2f2f6d656469612e646973636f72646170702e6e65742f6174746163686d656e74732f3838393537333335393131313737343332392f313330363037343537353334373531353531342f696d6167652e706e673f65783d36373335353833632669733d363733343036626326686d3d38666431366633306239393161303931646338666234373933643032663466663034316364643035643935376637643439656136346232653763616139353930263d26666f726d61743d77656270267175616c6974793d6c6f73736c6573732677696474683d353033266865696768743d353033" width=500/>
</div>

```
Hello! 🌟 How can I assist you today?
Your first message was: "Hello" 😊. How can I help you further?
The file depicts a photo of two individuals posing together in a dimly lit environment, possibly at a social gathering or event. The background contains some lights, suggesting a lively atmosphere. One person is wearing a dark jacket, while the other has long hair and is dressed in a black top. The overall mood of the image appears to be casual and cheerful. 🎉😊
```
