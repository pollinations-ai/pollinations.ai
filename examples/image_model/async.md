```python
import pollinations
import asyncio

async def async_test():
    image_model = pollinations.Async.Image()

    await image_model(
        prompt="A black cat in a cyberpunk city."
    )
    await image_model.save(
        file="pollinations-image.png"
    )

asyncio.run(async_test())
```

<div id="header">
  <img src="https://i.ibb.co/m60BGZ3/image.png" width=500/>
</div>
