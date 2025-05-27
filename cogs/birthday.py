from datetime import datetime, date

from discord.ext import commands, tasks

from config import BIRTHDAY_TIME, BIRTHDAY_CHANNEL_ID, BIRTHDAY_FILE
from utils.birthday_utils import get_all_birthdays, get_birthday_by_user_id, set_birthday_for_user_id
from utils.logger import logger


class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.birthday_channel_id = BIRTHDAY_CHANNEL_ID
        self.check_birthdays.start()

    @commands.command()
    async def setbirthday(self, ctx: commands.Context, date: str) -> None:
        """set your birthday using DD-MM format"""
        logger.info(f"setbirthday command called by user {ctx.author}")
        try:
            datetime.strptime(date, "%d-%m")
            set_birthday_for_user_id(BIRTHDAY_FILE, ctx.author.id, date)
            await ctx.send(f"birthday set to {date}")
            logger.info(f"user {ctx.author}'s birthday set to {date}")
        except ValueError:
            logger.error(f"invalid birthday format sent by user {ctx.author}")
            await ctx.send("invalid format, please use DD-MM")

    @commands.command()
    async def mybirthday(self, ctx: commands.Context) -> None:
        """check your birthday"""
        logger.info(f"mybirthday command called by user {ctx.author}")
        bday = get_birthday_by_user_id(BIRTHDAY_FILE, ctx.author.id)
        await ctx.send(f"your birthday currently is set to: {bday}")

    @commands.command()
    async def birthdays(self, ctx: commands.Context) -> None:
        """sends all birthdays"""
        logger.info(f"birthdays command called by user {ctx.author}")
        message = "__BIRTHDAYS:__ \n"
        for user_id, birthday in get_all_birthdays(BIRTHDAY_FILE).items():
            try:
                user = await self.bot.fetch_user(user_id)
                bday = datetime.strptime(birthday, "%d-%m")
                message += f"**{user.display_name}**: {bday.strftime('%d %B')} \n"
            except ValueError:
                logger.error(f"invalid birthday format for user {user.display_name}: {birthday}")
                await ctx.send(f"invalid birthday format for user {user.display_name}: {birthday}, please set to DD-MM")

        await ctx.send(message)

    @tasks.loop(time=BIRTHDAY_TIME)
    async def check_birthdays(self) -> None:
        """checks if it's someone's birthday and sends a message."""
        current_date = date.today()
        birthday_channel = self.bot.get_channel(self.birthday_channel_id)

        if not birthday_channel:
            logger.error(f"birthday channel with id {self.birthday_channel_id} not found")

        for user_id, birthday in get_all_birthdays(BIRTHDAY_FILE).items():
            try:
                logger.debug(f"fetching user with id {user_id}")
                user = await self.bot.fetch_user(user_id)
                logger.debug(f"user fetched: {user}")
                bday = datetime.strptime(birthday, "%d-%m")
                logger.debug(f"checking user {user.display_name} with birthday {bday}")
                if bday.month == current_date.month and bday.day == current_date.day:
                    logger.info(f"user {user.display_name} birthday is the same as current date")
                    await birthday_channel.send(f"today's {user.display_name} birthday!")
            except ValueError:
                logger.error(f"invalid birthday format for user {user.display_name}: {birthday}")
                await birthday_channel.send(
                    f"invalid birthday format for user {user.display_name}: {birthday}, please set to DD-MM"
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))
