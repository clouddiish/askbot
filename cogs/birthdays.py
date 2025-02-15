from datetime import datetime, date, timedelta

from discord.ext import commands, tasks

from data.birthdays import birthdays
from config import BIRTHDAY_TIME, GAYNERAL_ID
from utils.logger import logger


class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_channel_id = GAYNERAL_ID
        self.check_birthdays.start()

    # @commands.command()
    # async def set_birthday(self, ctx, date: str):
    #     """Set your birthday using DD-MM format"""
    #     logger.info(f"set_birthday command called by user {ctx.author}")
    #     try:
    #         bday = datetime.strptime(date, "%d-%m")
    #         birthdays[ctx.author.id] = bday
    #         await ctx.send(f"birthday set to {bday.strftime("%d %B")}")
    #         logger.info(f"user {ctx.author}'s birthday set to {bday}")
    #     except ValueError:
    #         logger.error(f"invalid birthday format sent by user {ctx.author}")
    #         await ctx.send("invalid format, please use DD-MM")

    @commands.command()
    async def birthdays(self, ctx):
        """Sends all birthdays"""
        logger.info(f"birthdays command called by user {ctx.author}")
        message = "__BIRTHDAYS:__ \n"
        for user_id, birthday in birthdays.items():
            user = await self.bot.fetch_user(user_id)
            message += f"**{user.display_name}**: {birthday.strftime("%d %B")} \n"

        await ctx.send(message)

    @tasks.loop(time=BIRTHDAY_TIME)
    async def check_birthdays(self):
        """Checks if it's someone's birthday and sends a message."""
        current_date = date.today()
        birthday_channel = self.bot.get_channel(self.birthday_channel_id)

        if not birthday_channel:
            logger.error(f"channel with id {self.birthday_channel_id} not found")

        for user_id, birthday in birthdays.items():
            logger.debug(f"fetching user with id {user_id}")
            user = await self.bot.fetch_user(user_id)
            logger.debug(f"user fetched: {user}")
            logger.debug(f"checking user {user.display_name} with birthday {birthday}")
            if birthday.month == current_date.month and birthday.day == current_date.day:
                logger.info(f"user {user.display_name} birthday is the same as current date")
                await birthday_channel.send(f"today's {user.display_name} birthday!")


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
