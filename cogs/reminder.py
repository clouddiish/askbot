from datetime import datetime

from discord.ext import commands, tasks

from config import REMINDER_CHANNEL_ID, REMINDER_FILE
from services import ReminderService
from utils.logger import logger


class Reminder(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reminder_service = ReminderService(reminder_filepath=REMINDER_FILE)

    @commands.Cog.listener()
    async def on_ready(self):
        """ensures the task starts only when the bot is fully ready"""
        logger.info("on_ready() of Reminder cog start")
        logger.debug("getting reminder channel")
        self.reminder_channel = self.bot.get_channel(REMINDER_CHANNEL_ID)
        if not self.reminder_channel:
            logger.error(f"reminder channel with id {REMINDER_CHANNEL_ID} not found")
        logger.debug(f"reminder channel gotten: {self.reminder_channel}")

        if not self.check_reminders.is_running():
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
            self.reminder_service.create_reminder(text=text, remind_at=remind_at_dt, to_remind=to_remind)
            await ctx.send(
                f'you asked to remind **{"everyone" if everyone.lower() == "yes" else ctx.author.name}** at **{remind_at}** with the text: **{text}**'
            )
        except ValueError:
            logger.error(f"invalid remind_at string {remind_at} sent by user {ctx.author}")
            await ctx.send(f"invalid datetime provided, please use a future date in the format YYYY-MM-DDThh:mm")
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-(")

    async def _get_readable_reminders(self, reminders: list[dict[str, str | int]]) -> str:
        readable_reminders = ""
        for reminder in reminders:
            if reminder["to_remind"] != "everyone":
                user = await self.bot.fetch_user(reminder["to_remind"])
                to_remind_readable = user.display_name
            else:
                to_remind_readable = reminder["to_remind"]
            readable_reminders += f'- {reminder["id"]}: **{reminder["text"]}**, remind at: **{reminder["remind_at"]}** to **{to_remind_readable}** \n'
        return readable_reminders

    @commands.command()
    async def allreminders(self, ctx: commands.Context) -> None:
        """displays all reminders"""
        logger.info(f"allreminders command called by user {ctx.author}")
        try:
            message = "__ALL REMINDERS:__ \n"
            readable_reminders = await self._get_readable_reminders(self.reminder_service.get_all_reminders())
            message += readable_reminders
            await ctx.send(message)
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-(")

    @commands.command()
    async def myreminders(self, ctx: commands.Context) -> None:
        """displays your reminders"""
        logger.info(f"myreminders command called by user {ctx.author}")
        try:
            message = "__YOUR REMINDERS:__ \n"
            readable_reminders = await self._get_readable_reminders(
                self.reminder_service.get_reminders_by_user_id(ctx.author.id)
            )
            message += readable_reminders
            await ctx.send(message)
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-( please try again!")

    @commands.command()
    async def delreminder(self, ctx: commands.Context, reminder_id: str) -> None:
        """deletes a reminder by given id"""
        logger.info(f"delreminder command called by user {ctx.author}")
        try:
            target_reminder = self.reminder_service.get_reminder_and_index_by_id(int(reminder_id))[1]
            if target_reminder["to_remind"] not in ["everyone", ctx.author.id]:
                await ctx.send(f"you can only delete your reminders or reminders to everyone")
                return
            self.reminder_service.delete_reminder_by_id(int(reminder_id))
            await ctx.send(f"deleted reminder with id {reminder_id}")
        except ValueError:
            logger.error(f"wrong id provided for reminder: {reminder_id}")
            await ctx.send("please provide a valid numeric id")
        except KeyError:
            logger.error(f"reminder with id {reminder_id} not found")
            await ctx.send(f"reminder with id {reminder_id} not found")
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await ctx.send("ow something went wrong :-(")

    @tasks.loop(seconds=30)
    async def check_reminders(self) -> None:
        logger.debug("check_reminders() start")
        try:
            current_dt = datetime.now().replace(second=0, microsecond=0)

            for reminder in self.reminder_service.get_all_reminders():
                remind_at_dt = datetime.strptime(reminder["remind_at"], "%Y-%m-%dT%H:%M:%S")
                if current_dt == remind_at_dt:
                    if reminder["to_remind"] == "everyone":
                        await self.reminder_channel.send(f'reminder to @everyone: **{reminder["text"]}**')
                        self.reminder_service.delete_reminder_by_id(int(reminder["id"]))
                    else:
                        user = await self.bot.fetch_user(reminder["to_remind"])
                        await self.reminder_channel.send(f'reminder to {user.mention}: **{reminder["text"]}**')
                        self.reminder_service.delete_reminder_by_id(int(reminder["id"]))
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            await self.reminder_channel.send("ow something went wrong :-(")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Reminder(bot))
