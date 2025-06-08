from datetime import datetime
import json

from utils.logger import logger


class ReminderService:
    def __init__(self, reminder_filepath: str) -> None:
        self.reminder_filepath = reminder_filepath

    def get_all_reminders(self) -> list[dict[str, str | int]]:
        logger.debug("getting all reminders")
        with open(self.reminder_filepath, "r") as file:
            reminders = json.load(file)
        return reminders

    def get_reminders_by_user_id(self, user_id: int) -> list[dict[str, str | int]]:
        logger.debug(f"getting reminders for user with id {user_id}")
        reminders = self.get_all_reminders()
        user_reminders = []
        for reminder in reminders:
            if reminder["to_remind"] in ["everyone", user_id]:
                user_reminders.append(reminder)
        return user_reminders

    def get_reminder_and_index_by_id(self, reminder_id: int) -> tuple[int, dict[str, str | int]]:
        logger.debug(f"getting reminder with id {reminder_id}")
        reminders = self.get_all_reminders()
        for i, reminder in enumerate(reminders):
            if reminder["id"] == reminder_id:
                return i, reminder
        logger.error(f"reminder with id {reminder_id} not found")
        raise KeyError(f"Reminder with id {reminder_id} not found")

    def _is_remind_at_in_the_future(self, remind_at: datetime) -> bool:
        now_dt = datetime.now()
        if remind_at < now_dt:
            return False
        return True

    def create_reminder(self, text: str, remind_at: datetime, to_remind: str | int) -> dict[str, str | int]:
        logger.debug(f"creating reminder with text {text}, remind_at {remind_at} and to_remind {to_remind}")
        if not self._is_remind_at_in_the_future(remind_at):
            logger.error(f"remind_at {remind_at} is in the past")
            raise ValueError("Remind_at is in the past")
        reminders = self.get_all_reminders()
        highest_id = max([reminder["id"] for reminder in reminders]) if reminders else 0
        new_reminder = {"id": highest_id + 1, "text": text, "remind_at": remind_at.isoformat(), "to_remind": to_remind}
        reminders.append(new_reminder)
        with open(self.reminder_filepath, "w") as file:
            json.dump(reminders, file, indent=2)
        return new_reminder

    def delete_reminder_by_id(self, reminder_id: int) -> str:
        logger.debug(f"deleting reminder with id {reminder_id}")
        index = self.get_reminder_and_index_by_id(reminder_id)[0]
        reminders = self.get_all_reminders()
        del reminders[index]
        with open(self.reminder_filepath, "w") as file:
            json.dump(reminders, file, indent=2)
        return f"Successfully deleted reminder with id {reminder_id}"
