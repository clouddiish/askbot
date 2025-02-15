from datetime import date, timedelta

import discord
from discord.ext import commands, tasks

from config import HANGOUT_POLL_DAY, HANGOUT_POLL_TIME, EVENTS_ID
from utils.general import get_sundays_of_month
from utils.logger import logger


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events_channel_id = EVENTS_ID
        self.hangout_poll_time = HANGOUT_POLL_TIME
        self.hangout_poll_day = HANGOUT_POLL_DAY
        self.send_hangout_poll.start()

    @tasks.loop(time=HANGOUT_POLL_TIME)
    async def send_hangout_poll(self):
        """Sends hangout poll at the specified day"""
        logger.debug("send hangout poll start")
        current_date = date.today()
        logger.debug(f"current day gotten: {current_date}")

        if current_date.day != self.hangout_poll_day:
            logger.debug("today is not the hangout poll day")
            return

        events_channel = self.bot.get_channel(self.events_channel_id)
        if not events_channel:
            logger.error(f"channel with id {self.events_channel_id} not found")
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


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
