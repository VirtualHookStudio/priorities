import unittest
import dotenv

from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

from app.src.sites.site_candleio import siteCandleIo
from app.src.sites.site_spider_moon import siteSpiderMoon
from app.src.sites.site_potato_books import sitePotatoBooks
from app.src.aws.dynamodb_access import DynamoDBAccess
from app.src.aws.s3_access import S3Access
from app.lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.users.users.DynamoDBAccess')
        self.addCleanup(p1.stop)
        self.MockDynamoDBAccess = p1.start()
        mock_dynamodb_instance = MagicMock(spec=DynamoDBAccess)
        self.MockDynamoDBAccess.return_value = mock_dynamodb_instance
        mock_dynamodb_instance.put_item.return_value = {"result": "success"}

        p2 = patch('app.lambda_function.S3Access')
        self.addCleanup(p2.stop)
        self.MockS3Access = p2.start()
        mock_s3_access_instance = MagicMock(spec=S3Access)
        self.MockS3Access.return_value = mock_s3_access_instance
        mock_s3_access_instance.upload_file.return_value = None

        p3 = patch('app.lambda_function.siteFactory')
        self.addCleanup(p3.stop)
        self.MockSiteFactory = p3.start()

        self.sites_mocks = {
            "candleio": MagicMock(spec=siteCandleIo),
            "potatobooks": MagicMock(spec=sitePotatoBooks),
            "spidermoon": MagicMock(spec=siteSpiderMoon),
        }

        for site_name, mock_instance in self.sites_mocks.items():
            mock_instance.requester.return_value = {"status": "ok", "site": site_name}
        
        self.MockSiteFactory.get_site_instance.side_effect = lambda site_name:self.sites_mocks[site_name]


    def test_lambda_handler_success_flow(self):

        event = {
            "id": "123456",
            "permission": 1,
            "name": "Test Name",
            "email": "testmessage@test.com",
            "password": "#oIn#@1cbAzs)85",
            "date_birth": "10-10-2000",
            "method": "CREATE",
            "sites": {
                "candleio": {
                    "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                    "taskId": 123123123,
                    "file": []
                }, 
                "spidermoon": {
                    "taskId": 123123123,
                    "prod": "verified",
                    "mat": "protocol_1233213",
                    "system": {"name": "theme", "value": "terror"},
                    "files": []
                }, 
                "potatobooks": {
                    "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                    "taskId": 5656565656,
                    "status": 5482354,
                    "config": {"name": "theme", "value": "terror"},
                    "file": []
                }}
        }

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)

        self.assertGreaterEqual(self.MockSiteFactory.get_site_instance.call_count, 1)
        self.assertLessEqual(self.MockSiteFactory.get_site_instance.call_count, 3)
        self.MockS3Access.return_value.upload_file.assert_called_once()
        self.MockDynamoDBAccess.return_value.put_item.assert_called_once()

    def test_lambda_handler_failure_flow(self):
        event = {}

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('body', result)

        self.assertEqual(self.MockSiteFactory.get_site_instance.call_count, 0)
        self.MockS3Access.return_value.upload_file.assert_not_called()
        self.MockDynamoDBAccess.return_value.put_item.assert_not_called()

    def test_lambda_handler_minimum_sites_count(self):
        event = {
            "id": "123456",
            "permission": 1,
            "name": "Test Name",
            "email": "test@example.com",
            "password": "testpassword",
            "date_birth": "10-10-2000",
            "method": "CREATE",
            "sites": {
                "candleio": {
                    "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                    "taskId": 123123123,
                    "file": []
                }, 
            }
        }

        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)

        self.assertEqual(self.MockSiteFactory.get_site_instance.call_count, 1)
        self.MockS3Access.return_value.upload_file.assert_called_once()
        self.MockDynamoDBAccess.return_value.put_item.assert_called_once()

if __name__ == '__main__':
    unittest.main()

