import asyncio
import logging

import discord
from discord.ext import commands

from config import TOKEN
from utils.logger import logger


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord")


async def load_cogs():
    """Loads all cogs"""
    cogs = ["cogs.minecraft", "cogs.birthdays", "cogs.events", "cogs.general"]
    for cog in cogs:
        try:
            logger.debug(f"loading cog {cog}")
            await bot.load_extension(cog)
            logger.debug(f"successfuly loaded cog {cog}")
        except Exception as e:
            logger.error(f"failed to load cog {cog}: {e}")


async def main():
    """Main async function to start the bot"""
    async with bot:
        await load_cogs()
        logger.info("All cogs loaded. Starting the bot...")
        await bot.start(TOKEN)


if __name__ == "__main__":
    discord.utils.setup_logging(level=logging.INFO)
    asyncio.run(main())  # Properly runs the async function
