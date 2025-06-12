from discord.ext import commands

from utils.decorators import catch_generic_exception
from utils.logger import logger


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @catch_generic_exception()
    async def whoareyou(self, ctx: commands.Context) -> None:
        """responds with im szłotych"""
        logger.info(f"whoareyou command called by user {ctx.author}")
        await ctx.send("im szłotych!")

    @commands.command()
    @catch_generic_exception()
    async def doyouloveus(self, ctx: commands.Context) -> None:
        """tells us it loves us"""
        logger.info(f"doyouloveus command called by user {ctx.author}")
        await ctx.send("I LOVE YOU ALL!!!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
