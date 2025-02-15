import discord
from discord.ext import commands

from ..utils.logger import logger


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoareyou(self, ctx):
        """Responds with im szłotych"""
        logger.info(f"whoareyou command called by user {ctx.author}")
        await ctx.send("im szłotych!")


async def setup(bot):
    await bot.add_cog(General(bot))
