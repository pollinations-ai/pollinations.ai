import pollinations

import asyncio

text_model = pollinations.Text()

async def main() -> None:
    async for token in await text_model.Async("This is a test.", stream=True):
        print(token, end="", flush=True)

    print()
    
asyncio.run(main())
