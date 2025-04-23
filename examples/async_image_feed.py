import pollinations

import asyncio

feed = pollinations.Feed(
    type="image",
    max_data=10  # Optional: If None then will be indefinite
)

async def main() -> None:
    async for item in feed.Async(): 
        print(len(feed.data), item, item["width"])
        
asyncio.run(main())
