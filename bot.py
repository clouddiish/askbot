from datetime import date, timedelta

import discord
from discord.ext import commands, tasks

from config import (
    TOKEN,
    GUILD_ID,
    EVENTS_ID,
    GAYNERAL_ID,
    GAYMING_ID,
    BIRTHDAY_TIME,
    HANGOUT_POLL_DAY,
    HANGOUT_POLL_TIME,
)
from data.birthdays import birthdays
from utils.dc_utils import *
from utils.logger import logger
from utils.general_utils import get_sundays_of_month
from utils.mc_utils import *


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    logger.debug(f"{bot.user} has connected to Discord")
    set_current_mc_players_channels.start()
    send_birthday_message.start()
    send_hangout_poll.start()


@tasks.loop(seconds=30)
async def set_current_mc_players_channels():
    logger.debug("getting guild")
    guild = bot.get_guild(GUILD_ID)
    logger.debug(f"guild gotten: {guild}")

    gayming_channel = bot.get_channel(GAYMING_ID)

    mcserver_category = get_mcserver_category(guild)
    mcserver_channels_set = get_mcserver_channels_set(mcserver_category)
    mcserver_players_set = get_mcserver_players_set()

    logger.debug("comparing mcserver channels set with mcserver players set")
    if mcserver_channels_set != mcserver_players_set:

        if len(mcserver_channels_set) < len(mcserver_players_set):
            await gayming_channel.send("Somebody joined the minecraft server!")

        logger.debug("clearing mcserver channels")
        await clear_mcserver_channels(mcserver_category)
        logger.debug("creating new mcserver channels")
        await update_mcserver_channels(mcserver_category)


@tasks.loop(time=BIRTHDAY_TIME)
async def send_birthday_message():
    logger.debug("Send birthday message start")
    current_date = date.today()
    logger.debug(f"Current date gotten: {current_date}")
    gayneral_channel = bot.get_channel(GAYNERAL_ID)

    for user_id, birthday in birthdays.items():
        logger.debug(f"Fetching user with id {user_id}")
        user = await bot.fetch_user(user_id)
        logger.debug(f"User fetched: {user}")
        logger.debug(f"Checking user {user.display_name} with birthday {birthday}")
        if birthday.month == current_date.month and birthday.day == current_date.day:
            logger.debug(f"User {user.display_name} birthday is the same as current date")
            await gayneral_channel.send(f"Today's {user.display_name} birthday!")


@bot.command(name="birthdays")
async def send_all_birthdays(ctx):
    message = "Birthdays: \n"
    for user_id, birthday in birthdays.items():
        user = await bot.fetch_user(user_id)
        message += f"{user.display_name}: {birthday} \n"

    await ctx.send(message)


@tasks.loop(time=HANGOUT_POLL_TIME)
async def send_hangout_poll():
    logger.debug("Send hangout poll start")
    current_date = date.today()
    logger.debug(f"Current day gotten: {current_date}")
    events_channel = bot.get_channel(EVENTS_ID)
    poll = discord.Poll(
        question="What do you choose?",
        duration=timedelta(days=7),
        multiple=True,
    )
    for day in get_sundays_of_month(current_date.year, current_date.month):
        poll.add_answer(text=str(day))
    logger.debug(f"Poll to be sent: {poll}")
    await events_channel.send("@everyone please vote when the next hangout should be")
    await events_channel.send(poll=poll)


bot.run(TOKEN)
