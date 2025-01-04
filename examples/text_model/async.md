```python
import pollinations
import asyncio

async def async_test():
    text_model = pollinations.Async.Text()

    await text_model(
        prompt="Hello.", 
        display=True,  # Simulates typing text.
        encode=True
    )

asyncio.run(async_test())
```

```
Hello! How can I assist you today?
```
