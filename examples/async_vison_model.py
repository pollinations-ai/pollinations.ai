import pollinations

import asyncio

text_model = pollinations.Text(
    model="openai",  # Use vision capable model
)

async def main() -> None:
    text_model.Image(["image.png", "image1.png"])  # text_model.Image("image.png") works as well
    print(await text_model("Describe the images"))
    
asyncio.run(main())
