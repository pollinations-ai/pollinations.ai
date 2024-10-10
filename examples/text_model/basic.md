```python
import pollinations

text_model: pollinations.TextModel = pollinations.text()
text_model.generate(
    prompt="Hello", 
    display=True # Simulates typing text.
)
# TextObject(...)
```

```
Hello! How can I assist you today?
```
