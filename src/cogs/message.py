import discord
from discord.ext import commands

class Message(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f"{message.author.name}: {message.content}")

def setup(bot: discord.Bot):
    bot.add_cog(Message(bot))