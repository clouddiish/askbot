from datetime import datetime
import json

from utils.logger import logger


class BirthdayService:
    def __init__(self, birthday_filepath: str) -> None:
        self.birthday_filepath = birthday_filepath

    def get_all_birthdays(self) -> dict[int, str]:
        logger.debug("getting all birthdays")
        with open(self.birthday_filepath, "r") as file:
            birthdays = json.load(file)
        birthdays = {int(user_id): birthdays[user_id] for user_id in birthdays}
        return birthdays

    def get_birthday_by_user_id(self, user_id: int) -> str:
        logger.debug(f"getting birthday of user with id {user_id}")
        birthdays = self.get_all_birthdays()
        if user_id in birthdays.keys():
            return birthdays[user_id]
        else:
            return "no birthday for this user"

    def set_birthday_for_user_id(self, user_id: int, birthday: str) -> None:
        datetime.strptime(birthday, "%d-%m")
        logger.debug(f"setting birthday of user with id {user_id} to {birthday}")
        birthdays = self.get_all_birthdays()
        birthdays.update({str(user_id): birthday})
        with open(self.birthday_filepath, "w") as file:
            json.dump(birthdays, file, indent=2)
