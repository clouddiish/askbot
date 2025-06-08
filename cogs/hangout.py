from datetime import date, timedelta

import discord
from discord.ext import commands, tasks

from config import HANGOUT_POLL_DAY, HANGOUT_POLL_TIME, HANGOUT_POLL_CHANNEL_ID, HANGOUT_POLL_WEEKDAY
from services import HangoutService
from utils.logger import logger


class Hangout(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.hangout_service = HangoutService()
        self.hangout_poll_time = HANGOUT_POLL_TIME
        self.hangout_poll_day = HANGOUT_POLL_DAY
        self.hangout_poll_weekday = HANGOUT_POLL_WEEKDAY

    @commands.Cog.listener()
    async def on_ready(self):
        """ensures the task starts only when the bot is fully ready"""
        logger.info("on_ready() of Hangout cog start")
        logger.debug("getting hangout channel")
        self.hangout_channel = self.bot.get_channel(HANGOUT_POLL_CHANNEL_ID)
        if not self.hangout_channel:
            logger.error(f"hangout channel with id {HANGOUT_POLL_CHANNEL_ID} not found")
        logger.debug(f"hangout channel gotten: {self.hangout_channel}")

        if not self.send_hangout_poll.is_running():
            self.send_hangout_poll.start()

    @tasks.loop(time=HANGOUT_POLL_TIME)
    async def send_hangout_poll(self) -> None:
        """sends hangout poll at the specified day"""
        logger.debug("send_hangout_poll() start")
        try:
            current_date = date.today()
            logger.debug(f"current day gotten: {current_date}")

            if current_date.day != self.hangout_poll_day:
                logger.debug("today is not the hangout poll day")
                return

            poll = discord.Poll(
                question="when should the next hangout be?",
                duration=timedelta(days=7),
                multiple=True,
            )
            for day in self.hangout_service.get_weekdays_of_month(
                current_date.year, current_date.month, self.hangout_poll_weekday
            ):
                poll.add_answer(text=str(day))
            logger.info(f"sending hangout poll: {poll}")
            await self.hangout_channel.send("@everyone please vote when the next hangout should be")
            await self.hangout_channel.send(poll=poll)
        except Exception as e:
            logger.error(f"unexpected error in send_hangout_poll(): {e}")
            await self.hangout_channel.send("ow something went wrong :-(")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hangout(bot))
