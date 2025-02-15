import discord
from discord.ext import commands, tasks

from config import GUILD_ID, MC_CATEGORY_ID, MCSERVER_IP, MC_CHANNEL_ID
from utils.dc import (
    get_mc_category_channels_set,
    clear_mc_category_channels,
    update_mc_category_channels,
)
from utils.logger import logger
from utils.mc import get_mcserver_players_set


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = GUILD_ID
        self.mc_category_id = MC_CATEGORY_ID
        self.gayming_id = MC_CHANNEL_ID
        self.mcserver_ip = MCSERVER_IP

    @commands.Cog.listener()
    async def on_ready(self):
        """ensures the task starts only when the bot is fully ready."""
        if not self.update_mc_players_channels.is_running():
            self.update_mc_players_channels.start()

    @tasks.loop(seconds=30)
    async def update_mc_players_channels(self):
        """updates the mc players channels to reflect actual current players in mcserver"""
        logger.debug("getting guild")
        guild = self.bot.get_guild(self.guild_id)
        logger.debug(f"guild gotten: {guild}")

        mc_category = discord.utils.get(guild.categories, id=self.mc_category_id)
        if not mc_category:
            logger.error(f"category with id {self.mc_category_id} not found")
            return

        mc_category_channels_set = get_mc_category_channels_set(mc_category)
        mcserver_players_set = get_mcserver_players_set()
        gayming_channel = self.bot.get_channel(self.gayming_id)

        logger.info("comparing mcserver channels set with mcserver players set")
        if mc_category_channels_set != mcserver_players_set:
            logger.info("updating mcserver channels")
            if len(mc_category_channels_set) < len(mcserver_players_set):
                await gayming_channel.send("somebody joined the minecraft server!")

            logger.debug("clearing mc_category channels")
            await clear_mc_category_channels(mc_category)
            logger.debug("creating new mc_category channels")
            await update_mc_category_channels(mc_category)


async def setup(bot):
    await bot.add_cog(Minecraft(bot))
