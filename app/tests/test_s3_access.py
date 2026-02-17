import unittest
from unittest.mock import patch, MagicMock

from app.src.aws.s3_access import S3Access

class TestS3Access(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.aws.s3_access.boto3.client')
        self.addCleanup(p1.stop)
        self.mock_boto_client = p1.start()
        self.mock_s3_client = MagicMock()
        self.mock_boto_client.return_value = self.mock_s3_client

        p2 = patch('app.src.aws.s3_access.Log')
        self.addCleanup(p2.stop)
        self.MockLog = p2.start()
        self.mock_log_instance = MagicMock()
        self.MockLog.return_value = self.mock_log_instance
        self.mock_log_instance.get_user.return_value = {
            "id": "123456", "email": "test@example.com", "name": "Test User"
        }
        self.mock_log_instance.get_method.return_value = "CREATE"
        self.mock_log_instance.get_time_info.return_value = "2024-01-01T00:00:00Z"

    def test_upload_file_success_flow(self):

        self.mock_s3_client.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        s3_access = S3Access()
        file_name = "test_file.json"
        data = {"key": "value"}

        s3_access.upload_file(file_name, data)

        self.mock_boto_client.assert_called_once_with('s3', region_name=s3_access.region)
        self.mock_s3_client.put_object.assert_called_once_with(Bucket=s3_access.bucket_name, Key=file_name, Body=unittest.mock.ANY)
    
    def test_upload_file_failure_flow(self):

        self.mock_s3_client.put_object.side_effect = Exception("S3 upload failure")

        s3_access = S3Access()
        file_name = "test_file"
        data = {}
        with self.assertLogs(level='ERROR') as log:
            s3_access.upload_file(file_name, data)
            self.assertIn("Error uploading file to S3: Missing required field: file_name or res", log.output[0])