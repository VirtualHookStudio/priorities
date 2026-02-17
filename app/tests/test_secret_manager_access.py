import unittest
from unittest.mock import patch, MagicMock

from app.src.aws.secret_manager_access import SecretManagerAccess

class TestDynamoDBAccess(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.aws.secret_manager_access.boto3.client')
        self.addCleanup(p1.stop)
        self.mock_boto_client = p1.start()
        self.mock_secrets_client = MagicMock()
        self.mock_boto_client.return_value = self.mock_secrets_client

    def test_get_secret_success_flow(self):

        self.mock_secrets_client.get_secret_value.return_value = {"SecretString": "secret_value"}

        secret_manager_access = SecretManagerAccess()
        secret_name = "test_secret"

        result = secret_manager_access.get_secret(secret_name)

        self.mock_boto_client.assert_called_once_with('secretsmanager', region_name=secret_manager_access.region)
        self.mock_secrets_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
        self.assertEqual(result, "secret_value")
    
    def test_get_secret_failure_flow(self):
        
        self.mock_secrets_client.get_secret_value.side_effect = Exception("Secrets Manager failure")

        secret_manager_access = SecretManagerAccess()
        secret_name = None

        with self.assertLogs(level='ERROR') as log:
            result = secret_manager_access.get_secret(secret_name)
            self.assertIn("Error retrieving secret: Secrets Manager failure", log.output[0])
            self.assertIsNone(result)