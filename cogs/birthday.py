from datetime import datetime, date

from discord.ext import commands, tasks

from config import BIRTHDAY_TIME, BIRTHDAY_CHANNEL_ID, BIRTHDAY_FILE
from services import BirthdayService
from utils.logger import logger


class Birthday(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bday_service = BirthdayService(birthday_filepath=BIRTHDAY_FILE)
        self.birthday_time = BIRTHDAY_TIME

    @commands.Cog.listener()
    async def on_ready(self):
        """ensures the task starts only when the bot is fully ready"""
        logger.info("on_ready() of Birthday cog start")
        logger.debug("getting birthday channel")
        self.birthday_channel = self.bot.get_channel(BIRTHDAY_CHANNEL_ID)
        if not self.birthday_channel:
            logger.error(f"birthday channel with id {BIRTHDAY_CHANNEL_ID} not found")
        logger.debug(f"birthday channel gotten: {self.birthday_channel}")

        if not self.check_birthdays.is_running():
            self.check_birthdays.start()

    @commands.command()
    async def setbirthday(self, ctx: commands.Context, date: str) -> None:
        """set your birthday using DD-MM format"""
        logger.info(f"setbirthday command called by user {ctx.author}")
        try:
            self.bday_service.set_birthday_for_user_id(ctx.author.id, date)
            await ctx.send(f"birthday set to {date}")
            logger.info(f"user {ctx.author}'s birthday set to {date}")
        except ValueError:
            logger.error(f"invalid birthday format sent by user {ctx.author}")
            await ctx.send("invalid format, please use DD-MM")
        except Exception as e:
            logger.error(f"unexpected error in setbirthday(): {e}")
            await ctx.send("ow something went wrong :-(")

    @commands.command()
    async def mybirthday(self, ctx: commands.Context) -> None:
        """check your birthday"""
        logger.info(f"mybirthday command called by user {ctx.author}")
        try:
            logger.info(f"mybirthday command called by user {ctx.author}")
            bday = self.bday_service.get_birthday_by_user_id(ctx.author.id)
            await ctx.send(f"your birthday currently is set to: {bday}")
        except Exception as e:
            logger.error(f"unexpected error in mybirthday(): {e}")
            await ctx.send("ow something went wrong :-(")

    @commands.command()
    async def allbirthdays(self, ctx: commands.Context) -> None:
        """send all birthdays"""
        logger.info(f"allbirthdays command called by user {ctx.author}")
        try:
            message = "__BIRTHDAYS:__ \n"
            for user_id, birthday in self.bday_service.get_all_birthdays().items():
                user = await self.bot.fetch_user(user_id)
                bday = datetime.strptime(birthday, "%d-%m")
                message += f"**{user.display_name}**: {bday.strftime('%d %B')} \n"
            await ctx.send(message)
        except ValueError:
            logger.error(f"invalid birthday format for user {user.display_name}: {birthday}")
            await ctx.send(f"invalid birthday format for user {user.display_name}: {birthday}, please set to DD-MM")
        except Exception as e:
            logger.error(f"unexpected error in allbirthdays(): {e}")
            await ctx.send("ow something went wrong :-(")

    @tasks.loop(time=BIRTHDAY_TIME)
    async def check_birthdays(self) -> None:
        """check if it's someone's birthday and sends a message."""
        logger.info("check_birthdays() start")
        try:
            current_date = date.today()
            for user_id, birthday in self.bday_service.get_all_birthdays().items():
                logger.debug(f"fetching user with id {user_id}")
                user = await self.bot.fetch_user(user_id)
                logger.debug(f"user fetched: {user}")
                bday = datetime.strptime(birthday, "%d-%m")
                logger.debug(f"checking user {user.display_name} with birthday {bday}")
                if bday.month == current_date.month and bday.day == current_date.day:
                    logger.info(f"user {user.display_name} birthday is the same as current date")
                    await self.birthday_channel.send(f"today's {user.display_name} birthday!")
        except ValueError:
            logger.error(f"invalid birthday format for user {user.display_name}: {birthday}")
            await self.birthday_channel.send(
                f"invalid birthday format for user {user.display_name}: {birthday}, please set to DD-MM"
            )
        except Exception as e:
            logger.error(f"unexpected error in check_birthdays(): {e}")
            await self.birthday_channel.send("ow something went wrong :-(")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Birthday(bot))
