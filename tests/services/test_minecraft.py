from unittest.mock import MagicMock, patch

import pytest

from services import MinecraftService


@pytest.fixture
def mock_mc_service() -> MagicMock:
    mock_mcserver = MagicMock()
    with patch("mcstatus.JavaServer.lookup", return_value=mock_mcserver):
        mock_mcserver.status = MagicMock()
        mock_mcserver.status.return_value.players.online = 5
        mock_mcserver.query = MagicMock()
        mock_mcserver.query.return_value.players.names = ["Player1", "Player2", "Player3"]

        mock_mc_service = MinecraftService()
        return mock_mc_service


class TestMinecraftService:
    def test_get_mcserver_players_counter(self, mock_mc_service: MagicMock) -> None:
        result = mock_mc_service.get_mcserver_players_counter()
        assert result == 5
        mock_mc_service.mcserver.status.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_mcserver_players_set(self, mock_mc_service: MagicMock) -> None:
        result = await mock_mc_service.get_mcserver_players_set()
        assert result == {"Player1", "Player2", "Player3"}
        mock_mc_service.mcserver.query.assert_called_once()
