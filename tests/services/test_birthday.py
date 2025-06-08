import pytest

from services import BirthdayService


@pytest.fixture
def prepopulated_birthday_file(tmp_path) -> str:
    file_path = tmp_path / "birthday_data.json"
    file_path.write_text('{"250367705079742464": "27-10"}')
    return file_path


class TestBirthdayService:
    def test_get_all_birthdays(self, prepopulated_birthday_file: str) -> None:
        bday_service = BirthdayService(birthday_filepath=prepopulated_birthday_file)
        birthdays = bday_service.get_all_birthdays()
        assert isinstance(birthdays, dict)
        assert len(birthdays) == 1

    def test_get_birthday_by_user_id_existing_bday(self, prepopulated_birthday_file: str) -> None:
        bday_service = BirthdayService(birthday_filepath=prepopulated_birthday_file)
        response = bday_service.get_birthday_by_user_id(250367705079742464)
        assert isinstance(response, str)
        assert response == "27-10"

    def test_get_birthday_by_user_id_nonexisting_bday(self, prepopulated_birthday_file: str) -> None:
        bday_service = BirthdayService(birthday_filepath=prepopulated_birthday_file)
        response = bday_service.get_birthday_by_user_id(123)
        assert isinstance(response, str)
        assert response == "no birthday for this user"

    def test_set_birthday_for_user_id_valid_date(self, prepopulated_birthday_file: str) -> None:
        bday_service = BirthdayService(birthday_filepath=prepopulated_birthday_file)
        bday_service.set_birthday_for_user_id(123, "13-03")
        new_birthdays = bday_service.get_all_birthdays()
        assert isinstance(new_birthdays, dict)
        assert len(new_birthdays) == 2

    def test_set_birthday_for_user_id_invalid_date(self, prepopulated_birthday_file: str) -> None:
        with pytest.raises(ValueError):
            bday_service = BirthdayService(birthday_filepath=prepopulated_birthday_file)
            bday_service.set_birthday_for_user_id(123, "abcd")
