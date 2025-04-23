import pollinations

import random
import discord
from discord.ext import commands

intents = discord.Intents.all()
text_model = pollinations.Text()
image_model = pollinations.Image()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def ask(ctx: commands.Context, *, prompt: str, **kwargs) -> None:
    message = await ctx.reply("Generating...")

    response = await text_model.Async(prompt)
    await message.edit(content=response)


@bot.command()
async def image(ctx: commands.Context, *, prompt: str, **kwargs) -> None:
    message = await ctx.reply("Generating...")

    image_model.file = f"{ctx.author.id}-{random.random()}.png"
    image = await image_model.Async(prompt)
    image.save(image_model.file)

    image = discord.File(image_model.file)
    await message.delete()
    await ctx.reply(content=f"`{prompt}`", file=image)


bot.run("TOKEN_HERE")
