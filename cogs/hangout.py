from datetime import date, timedelta

import discord
from discord.ext import commands, tasks

from config import HANGOUT_POLL_DAY, HANGOUT_POLL_TIME, HANGOUT_POLL_CHANNEL_ID
from utils.general_utils import get_sundays_of_month
from utils.logger import logger


class Hangout(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.hangout_poll_channel_id = HANGOUT_POLL_CHANNEL_ID
        self.hangout_poll_time = HANGOUT_POLL_TIME
        self.hangout_poll_day = HANGOUT_POLL_DAY
        self.send_hangout_poll.start()

    @tasks.loop(time=HANGOUT_POLL_TIME)
    async def send_hangout_poll(self) -> None:
        """sends hangout poll at the specified day"""
        logger.debug("send hangout poll start")
        current_date = date.today()
        logger.debug(f"current day gotten: {current_date}")

        if current_date.day != self.hangout_poll_day:
            logger.info("today is not the hangout poll day")
            return

        events_channel = self.bot.get_channel(self.hangout_poll_channel_id)
        if not events_channel:
            logger.error(f"channel with id {self.hangout_poll_channel_id} not found")
            return

        poll = discord.Poll(
            question="when should the next hangout be?",
            duration=timedelta(days=7),
            multiple=True,
        )
        for day in get_sundays_of_month(current_date.year, current_date.month):
            poll.add_answer(text=str(day))
        logger.info(f"sending hangout poll: {poll}")
        await events_channel.send("@everyone please vote when the next hangout should be")
        await events_channel.send(poll=poll)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hangout(bot))
