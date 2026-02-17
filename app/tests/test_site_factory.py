import unittest
from unittest.mock import MagicMock, patch

from app.src.factories.site_factory import siteFactory
from app.src.sites.site_potato_books import sitePotatoBooks
from app.src.sites.site_spider_moon import siteSpiderMoon
from app.src.sites.site_candleio import siteCandleIo

class TestSiteFactory(unittest.TestCase):

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

    def test_get_sites_success_flow(self):
        site_name = ["candleio", "potatobooks", "spidermoon"]

        for site in site_name:
            siteClass = siteFactory.get_site_instance(site)

            if site == "candleio":
                self.assertIsInstance(siteClass, siteCandleIo)
            elif site == "potatobooks":
                self.assertIsInstance(siteClass, sitePotatoBooks)
            elif site == "spidermoon":
                self.assertIsInstance(siteClass, siteSpiderMoon)

            self.assertEqual(
                siteClass.requester(
                    {
                        "Authorization": "Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                        "taskId": 123123123,
                        "prod": "verified",
                        "mat": "protocol_1233213",
                        "system": {"name": "theme", "value": "terror"},
                        "config": {"name": "theme", "value": "terror"},
                        "user": {
                            "id": 123456789,
                            "email" : "test@example.com"
                        },
                        "files": []
                    }
                ), 
                {"status": "ok", "site": "PASSED"}
            )
    
    def test_get_sites_failure_flow(self):
        with self.assertRaises(ValueError) as context:
            siteFactory.get_site_instance("invalid_site")
        
        self.assertEqual(str(context.exception), "Site None not found!")