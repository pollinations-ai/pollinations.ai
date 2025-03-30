```python
import pollinations

text_model = pollinations.Text(
    model="openai",
    contextual=True,
)  # or pollinations.Text()

while True:
    prompt: str = input("User:\n> ")
    print("\nPollinations:\n> ", end="")
    text_model.generate(
        prompt=prompt,
        display=True,
        encode=True
    )
    print()
```

```
User:
> Hi.

Pollinations:
> Hello! How can I assist you today?
```
