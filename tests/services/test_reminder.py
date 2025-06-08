from datetime import datetime, timedelta
import pytest

from services import ReminderService


@pytest.fixture
def prepopulated_reminder_file(tmp_path) -> str:
    file_path = tmp_path / "reminder_data.json"
    file_path.write_text(
        '[{"id": 1, "text": "test reminder", "remind_at": "2025-06-12T12:00:00", "to_remind": "everyone"}, {"id": 2, "text": "test reminder 2", "remind_at": "2025-06-12T12:00:00", "to_remind": 250367705079742464}]'
    )
    return file_path


class TestReminderService:
    def test_get_all_reminders(self, prepopulated_reminder_file: str) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        reminders = reminder_service.get_all_reminders()
        assert isinstance(reminders, list)
        assert len(reminders) == 2

    def test_get_reminders_by_user_id(self, prepopulated_reminder_file: str) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        reminders = reminder_service.get_reminders_by_user_id(250367705079742464)
        assert isinstance(reminders, list)
        assert len(reminders) == 2

    def test_get_reminder_and_index_by_id_ok(self, prepopulated_reminder_file: str) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        index, reminder = reminder_service.get_reminder_and_index_by_id(2)
        assert index == 1
        assert reminder["id"] == 2
        assert reminder["text"] == "test reminder 2"

    def test_get_reminder_and_index_by_id_wrong_id(self, prepopulated_reminder_file: str) -> None:
        with pytest.raises(KeyError):
            reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
            reminder_service.get_reminder_and_index_by_id(100)

    @pytest.mark.parametrize(
        "remind_at, expected_bool",
        [(datetime.now() + timedelta(days=1), True), ((datetime.now() - timedelta(days=1)), False)],
    )
    def test_is_remind_at_in_the_future(
        self, prepopulated_reminder_file: str, remind_at: datetime, expected_bool: bool
    ) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        result = reminder_service._is_remind_at_in_the_future(remind_at)
        assert result == expected_bool

    def test_create_reminder_ok(self, prepopulated_reminder_file: str) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        remind_at = datetime.now() + timedelta(days=1)
        reminder_service.create_reminder(text="test reminder 3", remind_at=remind_at, to_remind="everyone")
        reminders = reminder_service.get_all_reminders()
        assert isinstance(reminders, list)
        assert len(reminders) == 3
        assert reminders[2]["id"] == 3
        assert reminders[2]["text"] == "test reminder 3"
        assert reminders[2]["remind_at"] == remind_at.isoformat()
        assert reminders[2]["to_remind"] == "everyone"

    def test_create_reminder_date_in_the_past(self, prepopulated_reminder_file: str) -> None:
        with pytest.raises(ValueError) as err:
            reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
            remind_at = datetime.now() - timedelta(days=1)
            reminder_service.create_reminder(text="test reminder 3", remind_at=remind_at, to_remind="everyone")

    def test_delete_reminder_by_id_ok(self, prepopulated_reminder_file: str) -> None:
        reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
        reminder_service.delete_reminder_by_id(1)
        reminders = reminder_service.get_all_reminders()
        assert isinstance(reminders, list)
        assert len(reminders) == 1

    def test_delete_reminder_by_id_wrong_id(self, prepopulated_reminder_file) -> None:
        with pytest.raises(KeyError):
            reminder_service = ReminderService(reminder_filepath=prepopulated_reminder_file)
            reminder_service.delete_reminder_by_id(100)
