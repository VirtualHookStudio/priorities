from app.src.sites.generic_site import GenericSite
from app.src.sites.site_potato_books import sitePotatoBooks
from app.src.sites.site_spider_moon import siteSpiderMoon
from app.src.sites.site_candleio import siteCandleIo

class siteFactory:
    @staticmethod
    def get_site_instance(site_name: str) -> GenericSite:
        SITE_DICT = {
            "candleio": siteCandleIo,
            "potatobooks": sitePotatoBooks,
            "spidermoon": siteSpiderMoon,
        }
        site_class = SITE_DICT.get(site_name)

        if not site_class:
            raise ValueError(f"Site {site_class} not found!")

        return site_class()
