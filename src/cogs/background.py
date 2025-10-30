import discord
from discord.ext import commands

class Background(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

def setup(bot: discord.Bot):
    bot.add_cog(Background(bot))
