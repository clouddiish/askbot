from utils.logger import logger
from utils.mc_utils import *


def get_mcserver_category(guild):
    for category in guild.categories:
        if "MCSERVER" in str(category):
            return category


def get_mcserver_channels_set(category):
    logger.debug("getting mcserver channels set")
    set_of_channels = set()
    for channel in category.channels:
        set_of_channels.add(str(channel))
    logger.debug(f"curent set of mcserver channels: {set_of_channels}")
    return set_of_channels


async def clear_mcserver_channels(category):
    for channel in category.channels:
        logger.debug(f"deleting channel {str(channel)}")
        await channel.delete()


async def update_mcserver_channels(category):

    for player in get_mcserver_players_set():
        logger.debug(f"creating channel {str(player)}")

        await category.create_voice_channel(str(player))
