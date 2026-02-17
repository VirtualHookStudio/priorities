import unittest
from unittest.mock import MagicMock

from app.src.logs.log import Log

class TestLog(unittest.TestCase):

    def setUp(self):
        self.mock_user_instance = MagicMock()
        self.mock_user_instance.get_user.return_value = {
            "id": "123456",
            "email": "test@example.com",
            "name": "Test User",
        }
        self.mock_method = "CREATE"

    def test_set_user_success_flow(self):
        log = Log()
        log.set_user(self.mock_user_instance)
        log.set_method(self.mock_method)
        log.set_time_info()
        
        self.assertEqual(self.mock_user_instance.get_user(), log.get_user())
        self.assertEqual(self.mock_method, log.get_method())
        pattern = r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}"
        self.assertRegex(log.get_time_info(), pattern)
    
    def test_set_user_failure_flow(self):
        log = Log()
        with self.assertLogs(level='ERROR') as output:
            log.set_user(None)
            self.assertIn("User instance cannot be None", output.output[0])
    
    def test_set_method_failure_flow(self):
        log = Log()
        with self.assertLogs(level='ERROR') as output:
            log.set_method(None)
            self.assertIn("Method cannot be None", output.output[0])