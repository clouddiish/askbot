import os

from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

from utils.logger import logger
from utils.dc_utils import *
from utils.mc_utils import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "prod":
    GUILD_ID = int(os.getenv("ASKOWICZE_GUILD_ID"))
    GAYMING_ID = int(os.getenv("GAYMING_ID"))
elif ENVIRONMENT == "test":
    GUILD_ID = int(os.getenv("TEST_GUILD_ID"))
    GAYMING_ID = int(os.getenv("TEST_GAYMING_ID"))

bot = commands.Bot(intents=discord.Intents.default(), command_prefix="!")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord")
    set_current_mc_players_channels.start()


@tasks.loop(seconds=30)
async def set_current_mc_players_channels():
    logger.info("getting guild")
    guild = bot.get_guild(GUILD_ID)
    logger.info(f"guild gotten: {guild}")

    gayming_channel = bot.get_channel(GAYMING_ID)

    mcserver_category = get_mcserver_category(guild)
    mcserver_channels_set = get_mcserver_channels_set(mcserver_category)
    mcserver_players_set = get_mcserver_players_set()

    logger.info("comparing mcserver channels set with mcserver players set")
    if mcserver_channels_set != mcserver_players_set:

        if len(mcserver_channels_set) < len(mcserver_players_set):
            await gayming_channel.send("Somebody joined the minecraft server!")

        logger.info("clearing mcserver channels")
        await clear_mcserver_channels(mcserver_category)
        logger.info("creating new mcserver channels")
        await update_mcserver_channels(mcserver_category)


bot.run(TOKEN)
