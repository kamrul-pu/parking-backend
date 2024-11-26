"""
Test Custom Management Commands for sqlte 3
"""

from unittest.mock import patch
from sqlite3 import OperationalError as Sqlite3OpError
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
@patch("time.sleep")  # Mock time.sleep to avoid actual delays
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_sleep, patched_check):
        """Test waiting for database if database is ready"""

        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    # def test_wait_for_db_delay(self, patched_sleep, patched_check):
    #     """Test waiting for database when getting OperationalError"""

    #     # Define the side_effect logic
    #     def side_effect(*args, **kwargs):
    #         # Simulate OperationalError twice, then return True (database ready)
    #         if patched_check.call_count < 3:
    #             raise Sqlite3OpError  # Simulate Sqlite3OpError on first 2 calls
    #         elif patched_check.call_count < 6:
    #             raise OperationalError  # Simulate OperationalError on next 3 calls
    #         return True  # Return True after 5 calls (simulate DB is ready)

    #     # Assign the side_effect to the patched_check mock
    #     patched_check.side_effect = side_effect

    #     # Run the command
    #     call_command("wait_for_db")

    #     # Assert that the check method was called the expected number of times (6)
    #     self.assertEqual(patched_check.call_count, 6)

    #     # Ensure that the check method was called with the correct arguments
    #     patched_check.assert_called_with(databases=["default"])

    #     # Verify that time.sleep was called as well
    #     self.assertGreater(patched_sleep.call_count, 0)
