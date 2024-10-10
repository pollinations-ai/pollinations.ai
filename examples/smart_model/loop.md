```python
import pollinations

# Required:
pollinations.keys(serpapi="00eb274b9a7f5ead2c8415e749cb038351ef92ef549c2b15c0893416ac9d9df3") # https://serpapi.com/

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
