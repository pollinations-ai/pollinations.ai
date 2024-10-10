```python
import pollinations

# Required:
pollinations.keys(serpapi="your-api-key") # https://serpapi.com/

smart_model: pollinations.SmartModel = pollinations.smart()

smart_model.generate(
    prompt="Hi",
    display=True
)
smart_model.generate(
    prompt="What time is it in London?",
    display=True
)
smart_model.generate(
    prompt="Can you make an image of earth viewed from the moon.",
    display=True,provide_details=True
)
```

```
Hello! How's it going?
It's 8:50 PM on October 10, 2024, in London.
Generating your image of Earth viewed from the Moon!
```
<div id="header">
  <img src="https://camo.githubusercontent.com/33eaf244c34fca5711bf82abdd9b80116a909db8b1774f24fb0506f28c0de4ce/68747470733a2f2f696d6167652e706f6c6c696e6174696f6e732e61692f70726f6d70742f4372656174652061207374756e6e696e6720696d616765206f66204561727468206173207365656e2066726f6d20746865204d6f6f6e5c277320737572666163652e3f6e656761746976653d26736565643d393537353535373433312677696474683d31303234266865696768743d31303234266e6f6c6f676f3d5472756526707269766174653d54727565266d6f64656c3d666c75782d7265616c69736d26656e68616e63653d54727565" width=500/>
</div>
