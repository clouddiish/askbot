import asyncio

from mcstatus import JavaServer

from config import MCSERVER_IP
from utils.logger import logger


class MinecraftService:
    def __init__(self) -> None:
        logger.debug("getting mcserver")
        self.mcserver = JavaServer.lookup(MCSERVER_IP)
        logger.debug(f"mcserver gotten: {self.mcserver}")

    def get_mcserver_players_counter(self) -> int:
        status = self.mcserver.status()
        counter = status.players.online
        logger.debug(f"current player counter: {counter}")
        return counter

    async def get_mcserver_players_set(self) -> set[str]:
        logger.debug("getting mcserver players set")

        def query_players():
            try:
                players_set = set()
                query = self.mcserver.query()
                for player in query.players.names:
                    players_set.add(player)
                return players_set
            except Exception as e:
                logger.error(f"Failed to query mcserver: {e}")
                return set()

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, query_players)
