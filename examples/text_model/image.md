```python
import pollinations

text_model = pollinations.Text(
    model=pollinations.Text.openai().name,
    contextual=True,
    seed="random",
    system="You are a helpful AI Assistant... ",
    limit=20
)  # or pollinations.Text()

text_model.image(
    file="my_file.png"
)

text_model.generate(
    prompt="What is in this image?", 
    display=True  # Simulates typing text.
)  # Text.Object(...)
```

<div id="header">
  <img src="https://i.ibb.co/d0BCSGZ/image.png" width=500/>
</div>

```
The image features a beautiful cat with distinctive striped fur and large, expressive yellow eyes. The cat is surrounded by delicate pink flowers that create a soft and vibrant background. The combination of the cat and the flowers gives the image a serene and picturesque quality, showcasing the natural beauty of both the animal and the floral surroundings.
```
