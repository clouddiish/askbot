from unittest.mock import AsyncMock, MagicMock

import pytest

from services import DiscordService


@pytest.fixture
def mock_prepopulated_category() -> MagicMock:
    mock_channel_1 = MagicMock()
    mock_channel_1.__str__.return_value = "Channel One"
    mock_channel_1.delete = AsyncMock()

    mock_channel_2 = MagicMock()
    mock_channel_2.__str__.return_value = "Channel Two"
    mock_channel_2.delete = AsyncMock()

    mock_category = MagicMock()
    mock_category.channels = [mock_channel_1, mock_channel_2]
    mock_category.create_voice_channel = AsyncMock()

    return mock_category


class TestDiscordService:
    def test_get_category_channels_set(self, mock_prepopulated_category: MagicMock) -> None:
        dc_service = DiscordService()
        result = dc_service.get_category_channels_set(mock_prepopulated_category)
        assert result == {"Channel One", "Channel Two"}

    @pytest.mark.asyncio
    async def test_clear_category_channels(self, mock_prepopulated_category: MagicMock) -> None:
        dc_service = DiscordService()
        await dc_service.clear_category_channels(mock_prepopulated_category)
        mock_prepopulated_category.channels[0].delete.assert_awaited_once()
        mock_prepopulated_category.channels[1].delete.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_category_channels(self, mock_prepopulated_category) -> None:
        dc_service = DiscordService()
        await dc_service.create_category_channels(mock_prepopulated_category, {"Channel Three"})
        mock_prepopulated_category.create_voice_channel.assert_awaited_once_with("Channel Three")
