from mcstatus import JavaServer

from ..config import MCSERVER_IP
from logger import logger


logger.debug("getting mcserver")
MC_SERVER = JavaServer.lookup(MCSERVER_IP)
logger.debug(f"mcserver gotten: {MC_SERVER}")


def get_mcserver_players_counter():
    status = MC_SERVER.status()
    counter = status.players.online
    logger.debug(f"current player counter: {counter}")
    return counter


def get_mcserver_players_set():
    logger.debug("getting mcserver players set")
    players_set = set()
    query = MC_SERVER.query()
    for player in query.players.names:
        players_set.add(player)
    logger.debug(f"current mcserver players set: {players_set}")
    return players_set
