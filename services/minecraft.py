from mcstatus import JavaServer

from config import MCSERVER_IP
from utils.logger import logger


class MinecraftService:
    def __init__(self) -> None:
        logger.debug("getting mcserver")
        self.mcserver = JavaServer.lookup(MCSERVER_IP)
        logger.debug(f"mcserver gotten: {self.mcserver}")

    async def get_mcserver_players_counter(self) -> int:
        status = self.mcserver.status()
        counter = status.players.online
        logger.debug(f"current player counter: {counter}")
        return counter

    async def get_mcserver_players_set(self) -> set[str]:
        logger.debug("getting mcserver players set")
        players_set = set()
        query = self.mcserver.query()
        for player in query.players.names:
            players_set.add(player)
        logger.debug(f"current mcserver players set: {players_set}")
        return players_set
