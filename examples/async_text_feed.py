import pollinations

import asyncio

feed = pollinations.Feed(
    type="text",
    max_data=10  # Optional: If None then will be indefinite
)

async def main() -> None:
    async for item in feed.Async(): 
        print(len(feed.data), item, item.data["parameters"]["seed"])
        
asyncio.run(main())
