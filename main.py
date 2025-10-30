import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

token = os.getenv("DISCORD_TOKEN")

cogs_list = [
    'background',
    'message'
]

for cog in cogs_list:
    bot.load_extension(f'src.cogs.{cog}')

if __name__ == "__main__":
    bot.run(token)