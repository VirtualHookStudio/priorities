import logging

from app.src.sites.generic_site import GenericSite

class siteSpiderMoon(GenericSite):
    def __init__(self):
        super().__init__("spidermoon")

    def _build_headers(self, req, opt):
        return {
            "Content-Type": "application/json",
        }
    
    def _build_payload(self, req, opt):
        try:
            if not isinstance(req, dict):
                raise TypeError("req must be a dict")

            if "system" not in req:
                raise ValueError("Missing required key: system")

            if not isinstance(req["system"], dict):
                raise TypeError("system must be a dict")
        except (TypeError, ValueError) as e:
            logging.error(str(e))
            return

        return {
            "taskId": req.get("taskId", ""),
            "prod": req.get("prod", ""),
            "mat": req.get("mat", ""),
            "system": [
                {"name": req.get("system", "").get("name", "")},
                {"value": req.get("system", "").get("value", "")}
            ],
            "files": []
        }