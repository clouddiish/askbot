import json

from utils.logger import logger


def get_all_birthdays(file_path: str) -> dict[int:str]:
    logger.debug("getting all birthdays")
    with open(file_path, "r") as file:
        birthdays = json.load(file)

    birthdays = {int(user_id): birthdays[user_id] for user_id in birthdays}
    return birthdays


def get_birthday_by_user_id(file_path: str, user_id: int) -> str:
    logger.debug(f"getting birthday of user with id {user_id}")
    birthdays = get_all_birthdays(file_path)
    if user_id in birthdays.keys():
        return birthdays[user_id]
    else:
        return "no birthday for this user"


def set_birthday_for_user_id(file_path: str, user_id: int, birthday: str) -> None:
    logger.debug(f"setting birthday of user with id {user_id} to {birthday}")
    birthdays = get_all_birthdays(file_path)
    birthdays.update({user_id: birthday})
    birthdays = {str(user_id): birthdays[user_id] for user_id in birthdays}
    with open(file_path, "w") as file:
        json.dump(birthdays, file, indent=2)
