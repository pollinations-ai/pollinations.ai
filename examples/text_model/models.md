```python
import pollinations

pollinations.Text.models()

# Specific model info
print(pollinations.Text.openai())
print(pollinations.Text.openai().info())
```

```
(
  'model-1',
  'model-2',
  'model-3',
  ...
)

openai
{'name': 'openai', 'type': 'chat', 'censored': True, 'description': 'OpenAI GPT-4', 'base_model': True}
```
