from datetime import date, timedelta


def get_sundays_of_month(year: int, month: int) -> list[date]:
    # Get the first day of the month
    first_day = date(year, month, 1)

    # Find the first Sunday of the month
    first_sunday = first_day + timedelta(days=(6 - first_day.weekday()) % 7)

    # Generate all Sundays in the month
    sundays = []
    current_sunday = first_sunday
    while current_sunday.month == month:
        sundays.append(current_sunday)
        current_sunday += timedelta(days=7)

    return sundays
