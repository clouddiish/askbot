import os
import logging

import discord
from dotenv import load_dotenv

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

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    logger.info(f"{client.user} has connected to Discord")


client.run(TOKEN)
