import discord
from discord.ext import commands, tasks

from config import GUILD_ID, MC_CATEGORY_ID, MC_CHANNEL_ID
from services import DiscordService, MinecraftService
from utils.logger import logger


class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.dc_service = DiscordService()
        self.mc_service = MinecraftService()

    @commands.Cog.listener()
    async def on_ready(self):
        """ensures the task starts only when the bot is fully ready"""
        logger.info("on_ready() of Minecraft cog start")
        logger.debug("getting guild")
        self.guild = self.bot.get_guild(GUILD_ID)
        if not self.guild:
            logger.error(f"guild with id {GUILD_ID} not found")
            raise ValueError("Error getting guild from Minecraft cog")
        logger.debug(f"guild gotten: {self.guild}")

        logger.debug("getting mc category")
        self.mc_category = discord.utils.get(self.guild.categories, id=MC_CATEGORY_ID)
        if not self.mc_category:
            logger.error(f"category with id {MC_CATEGORY_ID} not found")
            raise ValueError("Error getting mc_category from Minecraft cog")
        logger.debug(f"mc category gotten: {self.mc_category}")

        logger.debug("getting mc channel")
        self.mc_channel = self.bot.get_channel(MC_CHANNEL_ID)
        if not self.mc_channel:
            logger.error(f"mc channel with id {MC_CHANNEL_ID} not found")
            raise ValueError("Error getting mc channel from Minecraft cog")
        logger.debug(f"mc channel gotten: {self.mc_channel}")

        if not self.update_mc_players_channels.is_running():
            self.update_mc_players_channels.start()

    @tasks.loop(seconds=30)
    async def update_mc_players_channels(self) -> None:
        """updates the mc players channels to reflect actual current players in mcserver"""
        logger.debug("update_mc_players_channels() start")
        try:
            mc_category_channels_set = self.dc_service.get_category_channels_set(category=self.mc_category)
            mcserver_players_set = await self.mc_service.get_mcserver_players_set()

            logger.debug("comparing mcserver channels set with mcserver players set")
            if mc_category_channels_set != mcserver_players_set:
                logger.info("updating mcserver channels")
                if len(mc_category_channels_set) < len(mcserver_players_set):
                    await self.mc_channel.send("somebody joined the minecraft server!")

                logger.debug("clearing mc_category channels")
                await self.dc_service.clear_category_channels(category=self.mc_category)
                logger.debug("creating new mc_category channels")
                await self.dc_service.create_category_channels(
                    category=self.mc_category, to_create=mcserver_players_set
                )
        except Exception as e:
            logger.error(f"unexpected error in update_mc_players_channels(): {e}")
            await self.mc_channel.send("ow something went wrong :-(")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Minecraft(bot))
