```python
import pollinations

text_model = pollinations.Text(
    model=pollinations.Text.openai().name,
    contextual=True,
    seed="random",
    system="You are a helpful AI Assistant... ",
    limit=20
)  # or pollinations.Text()

while True:
    prompt: str = input("User:\n> ")
    print("\nPollinations:\n> ", end="")
    text_model.generate(
        prompt=prompt,
        display=True
    )  # Text.Object(...)
    print()
```

```
User:
> Hi.

Pollinations:
> Hello! How can I assist you today?
```
