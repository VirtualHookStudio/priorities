import unittest
from unittest.mock import MagicMock, patch

from app.src.sites.site_candleio import siteCandleIo

class TestSiteCandleIO(unittest.TestCase):

    def setUp(self):
        p1 = patch('app.src.sites.generic_site.SecretManagerAccess')
        self.addCleanup(p1.stop)
        self.MockSecretManagerAccess = p1.start()
        mock_secret_manager_instance = MagicMock()
        self.MockSecretManagerAccess.return_value = mock_secret_manager_instance
        mock_secret_manager_instance.get_secret.return_value = "https://example.com/api"

        p2 = patch('app.src.sites.generic_site.requests.post')
        self.addCleanup(p2.stop)
        mock_post = p2.start()

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "ok", "site": "PASSED"}

        mock_post.return_value = mock_response

    def test_requester_success_flow(self):

        site_instance = siteCandleIo()
        
        self.assertEqual(
            site_instance.requester(
                {
                    "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                    "taskId": 123123123,
                    "files": []
                },
                {"user_id": 1}), 
            {"status": "ok", "site": "PASSED"}
        )

    def test_requester_failure_flow(self):

        site_instance = siteCandleIo()
        
        self.MockSecretManagerAccess.return_value.get_secret.side_effect = Exception("Secret not found")

        with self.assertLogs(level='ERROR') as log:
            site_instance.requester({}, {})
            self.assertRegex(
                log.output[0],
                r"opt must be a dict|Missing required key: user|user must be a dict"
            )