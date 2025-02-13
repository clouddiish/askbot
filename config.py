import os
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "prod":
    GUILD_ID = int(os.getenv("ASKOWICZE_GUILD_ID"))
    EVENTS_ID = int(os.getenv("EVENTS_ID"))
    GAYNERAL_ID = int(os.getenv("GAYNERAL_ID"))
    GAYMING_ID = int(os.getenv("GAYMING_ID"))

elif ENVIRONMENT == "test":
    GUILD_ID = int(os.getenv("TEST_GUILD_ID"))
    EVENTS_ID = int(os.getenv("TEST_EVENTS_ID"))
    GAYNERAL_ID = int(os.getenv("TEST_GAYNERAL_ID"))
    GAYMING_ID = int(os.getenv("TEST_GAYMING_ID"))

HANGOUT_POLL_DAY = 1
HANGOUT_POLL_TIME = time(hour=8, minute=0, tzinfo=ZoneInfo("Europe/Warsaw"))

BIRTHDAY_TIME = time(hour=8, minute=0, tzinfo=ZoneInfo("Europe/Warsaw"))

MCSERVER_IP = os.getenv("MCSERVER_IP")
