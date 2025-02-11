import os

from dotenv import load_dotenv
from mcstatus import JavaServer

from utils.logger import logger

load_dotenv()
logger.info("getting mcserver")
MC_SERVER = JavaServer.lookup(os.getenv("MCSERVER_IP"))
logger.info(f"mcserver gotten: {MC_SERVER}")


def get_mcserver_players_counter():
    status = MC_SERVER.status()
    counter = status.players.online
    logger.info(f"current player counter: {counter}")
    return counter


def get_mcserver_players_set():
    logger.info("getting mcserver players set")
    players_set = set()
    query = MC_SERVER.query()
    for player in query.players.names:
        players_set.add(player)
    logger.info(f"current mcserver players set: {players_set}")
    return players_set
