from datetime import datetime
import json

from utils.logger import logger


def get_all_reminders(file_path: str) -> list[dict[str, str | int]]:
    logger.debug("getting all reminders")
    with open(file_path, "r") as file:
        reminders = json.load(file)
    return reminders


def get_reminders_by_user_id(file_path: str, user_id: int) -> list[dict[str, str | int]]:
    logger.debug(f"getting reminders for user with id {user_id}")
    reminders = get_all_reminders(file_path)
    user_reminders = []
    for reminder in reminders:
        if reminder["to_remind"] in ["everyone", user_id]:
            user_reminders.append(reminder)
    return user_reminders


def _is_remind_at_in_the_future(remind_at: datetime) -> bool:
    now_dt = datetime.now()
    if remind_at < now_dt:
        return False
    return True


def create_reminder(file_path: str, text: str, remind_at: datetime, to_remind: str | int) -> dict[str, str | int]:
    logger.debug(f"creating reminder with text {text}, remind_at {remind_at} and to_remind {to_remind}")
    if not _is_remind_at_in_the_future(remind_at):
        logger.error(f"remind_at {remind_at} is in the past")
        raise ValueError("Remind_at is in the past")
    reminders = get_all_reminders(file_path)
    highest_id = max([reminder["id"] for reminder in reminders]) if reminders else 0
    new_reminder = {"id": highest_id + 1, "text": text, "remind_at": remind_at.isoformat(), "to_remind": to_remind}
    reminders.append(new_reminder)
    with open(file_path, "w") as file:
        json.dump(reminders, file, indent=2)
    return new_reminder


def get_reminder_and_index_by_id(file_path: str, reminder_id: int) -> tuple[int, dict[str, str | int]]:
    logger.debug(f"getting reminder with id {reminder_id}")
    reminders = get_all_reminders(file_path)
    for i, reminder in enumerate(reminders):
        if reminder["id"] == reminder_id:
            return i, reminder
    logger.error(f"reminder with id {reminder_id} not found")
    raise KeyError(f"Reminder with id {reminder_id} not found")


def delete_reminder_by_id(file_path: str, reminder_id: int) -> str:
    logger.debug(f"deleting reminder with id {reminder_id}")
    index, target_reminder = get_reminder_and_index_by_id(file_path, reminder_id)
    reminders = get_all_reminders(file_path)
    del reminders[index]
    with open(file_path, "w") as file:
        json.dump(reminders, file, indent=2)
    return f"Successfully deleted reminder with id {reminder_id}"


def update_reminder_by_id(
    file_path: str, reminder_id: int, new_text: str, new_remind_at: datetime, new_to_remind: str | int
) -> dict[str, str | int]:
    logger.debug(
        f"updating reminder with id {id} with text {new_text}, remind_at {new_remind_at} and to_remind {new_to_remind}"
    )
    if not _is_remind_at_in_the_future(new_remind_at):
        logger.error(f"remind_at {new_remind_at} is in the past")
        raise ValueError("Remind_at is in the past")
    delete_reminder_by_id(file_path, reminder_id)
    updated_reminder = create_reminder(file_path, new_text, new_remind_at, new_to_remind)
    return updated_reminder
