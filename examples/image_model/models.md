```python
import pollinations

pollinations.Image.models()

# Specific model info
print(pollinations.Image.flux())
print(pollinations.Image.flux().info())
```

```
(
  'model-1',
  'model-2',
  'model-3',
  ...
)

flux
{'name': 'flux', 'type': 'image', 'censored': False, 'description': 'Flux Model', 'base_model': True}
```
