import os
import logging

from dotenv import load_dotenv
import discord
from discord.ext import commands

# LOGGING

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

formatter = logging.Formatter("{asctime} {levelname} \t{message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# DISCORD BOT

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(intents=discord.Intents.default(), command_prefix="!")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord")


bot.run(TOKEN)
