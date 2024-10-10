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

while True:
    prompt: str = input("User:\n> "); print("\nPollinations:\n> ", end="")
    text_model.generate(
        prompt=prompt,
        display=True
    ); print()
    # TextObject(...)
```

```
User:
> Hi.

Pollinations:
> Hello! 😊 How can I assist you today?
```
