import unittest
from unittest.mock import patch, MagicMock

from app.src.aws.dynamodb_access import DynamoDBAccess

class TestDynamoDBAccess(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.aws.dynamodb_access.boto3.resource')
        self.addCleanup(p1.stop)
        self.mock_boto_resource = p1.start()

        self.mock_dynamodb = MagicMock()
        self.mock_table = MagicMock()

        self.mock_boto_resource.return_value = self.mock_dynamodb
        self.mock_dynamodb.Table.return_value = self.mock_table

    def test_put_item_success_flow(self):

        self.mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        dynamodb_access = DynamoDBAccess()
        item = {
            'id': '123456',
            'permission': 1,
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'secure_password',
            'date_birth': '1990-01-01'
        }

        dynamodb_access.put_item(item)

        self.mock_boto_resource.assert_called_once_with('dynamodb', region_name=dynamodb_access.region)
        self.mock_dynamodb.Table.assert_called_once_with(dynamodb_access.table_name)
        self.mock_table.put_item.assert_called_once_with(Item=item)
    
    def test_put_item_failure_flow(self):

        self.mock_table.put_item.side_effect = Exception("DynamoDB failure")

        dynamodb_access = DynamoDBAccess()
        item = {}
        with self.assertLogs(level='ERROR') as log:
            dynamodb_access.put_item(item)
            self.assertIn("Error inserting item: Missing required field: id", log.output[0])
        