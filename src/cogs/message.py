import discord
from discord.ext import commands
import re
from src.utils.kobold import KoboldClient

class Message(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.kobold_client = KoboldClient()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f"{message.author.name}: {message.content}")

        # prevent replies to itself
        if message.author.id == self.bot.user.id or message.author.bot:
            return
        
        if len(message.content) == 0:
            return
        
        user_msg = self.replace_user_mentions(message.content)

        if "glados" not in user_msg.lower():
            return
        
        self.kobold_client.write_to_history(message.author.name, user_msg)
        
        # Have glados reply if mentioned
        response = self.kobold_client.get_response(user_msg, message.author.name)
        response = self.trim_incomplete_sentence(response)
        self.kobold_client.write_to_history("Glados", response)
        
        await message.channel.send(response)


    @commands.slash_command()
    async def clear(self, ctx: discord.ApplicationContext):
        self.kobold_client.clear_memory()
        await ctx.respond("Memory Cleared...")


    def replace_user_mentions(self, message: str) -> str:
        """Replaces @<user> mentions with their discord usernames"""
        new_msg = ""
        mention_pattern = r"<@\d+>"
        result: list[str] = re.findall(mention_pattern, message)

        for x in result:
            # x is <@1234...>
            if x in message:
                id_pattern = r"<@(\d+)>"

                # extract just the number, omit <> and @
                result = re.findall(id_pattern, x)
                id = int(result[0])
                user = self.bot.get_user(id)
                if not user:
                    continue
                name = user.name
                new_msg = message.replace(x, name)
        
        # return old message if nothing got changed
        if not new_msg:
            return message
        
        # otherwise, return new message.
        return new_msg
    
    def trim_incomplete_sentence(self, response: str) -> str:
        """
        Trims any incomplete/broken sentence in a response.

        Parameters:
            response (str): The LLM response, that may consist of multiple sentences.
        Return:
            str: The LLM response free of any broken/incomplete sentence.
        """

        # for if the llm generated a single sentence w/ no punctuations
        if not any(char in response for char in '.!?'):
            return response

        # trim sentence to the last punctuation
        i = len(response) - 1
        while response[i] not in ('.', '!', '?'):
            i -= 1
        
        return response[:i+1]


def setup(bot: discord.Bot):
    bot.add_cog(Message(bot))