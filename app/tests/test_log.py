import unittest
from unittest.mock import MagicMock

from app.src.logs.log import Log

class TestLog(unittest.TestCase):

    def setUp(self):
        self.mock_user_instance = MagicMock()
        self.mock_user_instance.user.return_value = {
            "id": "123456",
            "email": "test@example.com",
            "name": "Test User",
        }
        self.mock_method = "CREATE"

    def test_set_user_success_flow(self):
        log = Log()
        log.user = self.mock_user_instance
        log.method = self.mock_method
        
        pattern = r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}"
        self.assertRegex(log.time_info, pattern)