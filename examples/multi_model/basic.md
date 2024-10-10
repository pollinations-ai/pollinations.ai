```python
import pollinations

multi_model: pollinations.MultiModel = pollinations.multi()

multi_model.generate(
    prompt="Hi",
    display=True
)
multi_model.generate(
    prompt="Can you make me an image of mario as an astronaut on the moon.",
    display=True,
)
```

```
Hello! How's it going?
Sure! Generating your image of Mario as an astronaut on the moon!
```
