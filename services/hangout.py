from datetime import date, timedelta


class HangoutService:
    def __init__(self) -> None:
        pass

    def get_weekdays_of_month(self, year: int, month: int, weekday: int) -> list[date]:
        """
        Return a list of all dates in the given month and year that fall on the specified weekday.

        Args:
            year (int): The year (e.g. 2025)
            month (int): The month (1-12)
            weekday (int): The weekday (0=Monday, ..., 6=Sunday)

        Returns:
            list[date]: List of date objects for the specified weekday in the month.
        """
        first_day = date(year, month, 1)
        first_target_day = first_day + timedelta(days=(weekday - first_day.weekday()) % 7)
        weekdays = []
        current = first_target_day
        while current.month == month:
            weekdays.append(current)
            current += timedelta(days=7)
        return weekdays
