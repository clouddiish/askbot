import discord

from utils.logger import logger


class DiscordService:
    def __init__(self) -> None:
        pass

    def get_category_channels_set(self, category: discord.CategoryChannel) -> set[str]:
        logger.debug(f"getting category {category} channels set")
        set_of_channels = set()
        for channel in category.channels:
            set_of_channels.add(str(channel))
        logger.debug(f"curent set of category channels: {set_of_channels}")
        return set_of_channels

    async def clear_category_channels(self, category: discord.CategoryChannel) -> None:
        for channel in category.channels:
            logger.debug(f"deleting channel {str(channel)}")
            await channel.delete()

    async def create_category_channels(self, category: discord.CategoryChannel, to_create: set[str]) -> None:
        for channel in to_create:
            logger.debug(f"creating channel {str(channel)}")
            await category.create_voice_channel(str(channel))
