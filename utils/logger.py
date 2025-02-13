import logging
import discord

logger = logging.getLogger("discord")
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

formatter = logging.Formatter("{asctime} {levelname} \t{message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
