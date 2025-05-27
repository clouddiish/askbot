from datetime import datetime

from discord.ext import commands, tasks

from config import REMINDER_CHANNEL_ID, REMINDER_FILE
from utils.reminder_utils import (
    get_all_reminders,
    get_reminders_by_user_id,
    create_reminder,
    delete_reminder_by_id,
    get_reminder_and_index_by_id,
)
from utils.logger import logger


class Reminder(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reminder_channel_id = REMINDER_CHANNEL_ID
        self.check_reminders.start()

    @commands.command()
    async def setreminder(self, ctx: commands.Context, remind_at: str, everyone: str, *, text: str) -> None:
        """set a reminder for yourself or everyone
        format must be: {datetime in the YYYY-MM-DDThh:mm format} {yes/no if notify everyone or just you} {text of the reminder}
        """
        logger.info(f"setreminder command called by user {ctx.author}")
        try:
            remind_at_dt = datetime.strptime(remind_at, "%Y-%m-%dT%H:%M")
            to_remind = "everyone" if everyone.lower() == "yes" else ctx.author.id
            create_reminder(REMINDER_FILE, text, remind_at_dt, to_remind)
            await ctx.send(
                f"you asked to remind **{"everyone" if everyone.lower() == "yes" else ctx.author.name}** at **{remind_at}** with the text: **{text}**"
            )
        except ValueError:
            logger.error(f"invalid remind_at string {remind_at} sent by user {ctx.author}")
            await ctx.send(f"invalid datetime provided, please use a future date in the format YYYY-MM-DDThh:mm")
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-( please try again!")

    @commands.command()
    async def allreminders(self, ctx: commands.Context) -> None:
        """displays all reminders"""
        logger.info(f"allreminders command called by user {ctx.author}")
        try:
            message = "__ALL REMINDERS:__ \n"
            for reminder in get_all_reminders(REMINDER_FILE):
                if reminder["to_remind"] != "everyone":
                    user = await self.bot.fetch_user(reminder["to_remind"])
                    to_remind_readable = user.display_name
                else:
                    to_remind_readable = reminder["to_remind"]
                message += f"- {reminder["id"]}: **{reminder["text"]}**, remind at: **{reminder["remind_at"]}** to **{to_remind_readable}** \n"
            await ctx.send(message)
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-( please try again!")

    @commands.command()
    async def myreminders(self, ctx: commands.Context) -> None:
        """displays your reminders"""
        logger.info(f"myreminders command called by user {ctx.author}")
        try:
            message = "__YOUR REMINDERS:__ \n"
            for reminder in get_reminders_by_user_id(REMINDER_FILE, ctx.author.id):
                if reminder["to_remind"] != "everyone":
                    user = await self.bot.fetch_user(reminder["to_remind"])
                    to_remind_readable = user.display_name
                else:
                    to_remind_readable = reminder["to_remind"]
                message += f"- {reminder["id"]}: **{reminder["text"]}**, remind at: **{reminder["remind_at"]}** to **{to_remind_readable}** \n"
            await ctx.send(message)
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-( please try again!")

    @commands.command()
    async def delreminder(self, ctx: commands.Context, reminder_id: str) -> None:
        """deletes a reminder by given id"""
        logger.info(f"delreminder command called by user {ctx.author}")
        try:
            index, target_reminder = get_reminder_and_index_by_id(REMINDER_FILE, reminder_id)
            if target_reminder["to_remind"] not in ["everyone", ctx.author.id]:
                await ctx.send(f"you can only delete your reminders or reminders to everyone")
                return
            delete_reminder_by_id(REMINDER_FILE, int(reminder_id))
            await ctx.send(f"deleted reminder with id {reminder_id}")
        except ValueError:
            logger.error(f"wrong id provided for reminder: {reminder_id}")
            await ctx.send("please provide a valid numeric id")
        except KeyError:
            logger.error(f"reminder with id {reminder_id} not found")
            await ctx.send(f"reminder with id {reminder_id} not found")
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-( please try again!")

    @tasks.loop(seconds=30)
    async def check_reminders(self) -> None:
        logger.info("checking for reminders")
        current_dt = datetime.now().replace(second=0, microsecond=0)
        reminder_channel = self.bot.get_channel(self.reminder_channel_id)
        if not reminder_channel:
            logger.error(f"reminder channel with id {self.reminder_channel_id} not found")

        for reminder in get_all_reminders(REMINDER_FILE):
            remind_at_dt = datetime.strptime(reminder["remind_at"], "%Y-%m-%dT%H:%M:%S")
            if current_dt == remind_at_dt:
                if reminder["to_remind"] == "everyone":
                    await reminder_channel.send(f"reminder to @everyone: **{reminder["text"]}**")
                    delete_reminder_by_id(REMINDER_FILE, int(reminder["id"]))
                else:
                    user = await self.bot.fetch_user(reminder["to_remind"])
                    await reminder_channel.send(f"reminder to {user.mention}: **{reminder["text"]}**")
                    delete_reminder_by_id(REMINDER_FILE, int(reminder["id"]))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Reminder(bot))
