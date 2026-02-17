import unittest
from unittest.mock import patch, MagicMock

from app.src.users.users import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.users.users.DynamoDBAccess')
        self.addCleanup(p1.stop)
        self.MockDynamoDBAccess = p1.start()
        mock_dynamodb_instance = MagicMock()
        self.MockDynamoDBAccess.return_value = mock_dynamodb_instance
        mock_dynamodb_instance.put_item.return_value = {"result": "success"}

    def test_create_user_success_flow(self):

        user = {
            "id": "123456",
            "permission": 1,
            "name": "Test Name",
            "email": "testmessage@test.com",
            "password": "#oIn#@1cbAzs)85",
            "date_birth": "10-10-2000",
            "method": "CREATE"
        }

        User(user)
        del user['method']

        self.MockDynamoDBAccess.return_value.put_item.assert_called_once_with(user)
    
    def test_create_user_failure_flow(self):

        user = {}

        User(user)

        self.MockDynamoDBAccess.return_value.put_item.assert_not_called()