from datetime import date
import pytest

from services import HangoutService


class TestHangoutService:
    @pytest.mark.parametrize(
        "weekday, expected_first",
        [
            (0, date(2025, 6, 2)),  # Monday
            (1, date(2025, 6, 3)),  # Tuesday
            (6, date(2025, 6, 1)),  # Sunday
        ],
    )
    def test_get_weekdays_of_month(self, weekday: int, expected_first: date) -> None:
        hangout_service = HangoutService()
        results = hangout_service.get_weekdays_of_month(2025, 6, weekday)
        assert results[0] == expected_first
