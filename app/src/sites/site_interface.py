from abc import ABC, abstractmethod
from typing import Dict

class siteInterface(ABC):
    @property
    @abstractmethod
    def site_name(self) -> str:
        pass
    
    @staticmethod
    @abstractmethod
    def compare(s, site: str) -> bool:
        pass

    @abstractmethod
    def _build_payload(self, req: dict) -> dict:
        pass

    @abstractmethod
    def _build_headers(self, req: dict) -> dict:
        pass

    @abstractmethod
    def requester(self, req: dict):
        pass
