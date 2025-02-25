import os
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "prod":
    GUILD_ID = int(os.getenv("GUILD_ID"))
    HANGOUT_POLL_CHANNEL_ID = int(os.getenv("HANGOUT_POLL_CHANNEL_ID"))
    BIRTHDAY_CHANNEL_ID = int(os.getenv("BIRTHDAY_CHANNEL_ID"))
    MC_CHANNEL_ID = int(os.getenv("MC_CHANNEL_ID"))
    MC_CATEGORY_ID = int(os.getenv("MC_CATEGORY_ID"))

elif ENVIRONMENT == "test":
    GUILD_ID = int(os.getenv("TEST_GUILD_ID"))
    HANGOUT_POLL_CHANNEL_ID = int(os.getenv("TEST_HANGOUT_POLL_CHANNEL_ID"))
    BIRTHDAY_CHANNEL_ID = int(os.getenv("TEST_BIRTHDAY_CHANNEL_ID"))
    MC_CHANNEL_ID = int(os.getenv("TEST_MC_CHANNEL_ID"))
    MC_CATEGORY_ID = int(os.getenv("TEST_MC_CATEGORY_ID"))

HANGOUT_POLL_DAY = 1
HANGOUT_POLL_TIME = time(hour=8, minute=0, tzinfo=ZoneInfo("Europe/Warsaw"))

BIRTHDAY_TIME = time(hour=8, minute=40, tzinfo=ZoneInfo("Europe/Warsaw"))
BIRTHDAY_FILE = "data/birthday_data.json"

MCSERVER_IP = os.getenv("MCSERVER_IP")
