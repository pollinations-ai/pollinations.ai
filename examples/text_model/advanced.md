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
```

```
Hello! 🌟 How can I assist you today?
Your first message was: "Hello" 😊. How can I help you further?
```
