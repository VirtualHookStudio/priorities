from app.src.sites.site_interface import siteInterface
from app.src.aws.secret_manager_access import SecretManagerAccess
import requests


class GenericSite(siteInterface):
  def __init__(self, site_name: str):
    self._secretmanager = SecretManagerAccess()
    self._site_name = site_name
    self._url = self._secretmanager.get_secret(f"{site_name.upper()}_URL")


  @property
  def site_name(self) -> str:
    return self._site_name

  
  def compare(self, site: str) -> bool:
    return self._site_name == site


  def _build_payload(self, req: dict, opt: dict = {}) -> dict:
    raise NotImplementedError("Each class must implement this method!")


  def _build_headers(self, req: dict, opt: dict = {}) -> dict:
    raise NotImplementedError("Each class must implement this method!")
  

  def requester(self, req: dict, opt: dict = {}) -> dict:
    payload = self._build_payload(req, opt)
    headers = self._build_headers(req, opt)
    
    try:
      response = requests.post(self._url, json=payload, headers=headers)
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"❌ {self.site_name}: {e}")
      return req