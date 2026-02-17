import logging

from app.src.sites.generic_site import GenericSite

class sitePotatoBooks(GenericSite):
    def __init__(self):
        super().__init__("potatobooks")

    def _build_headers(self, req, opt):
        return {
            "Content-Type": "application/json",
            "Authorizaton": req.get("Authorization")
        }

    def _build_payload(self, req, opt):
        try:
            if not isinstance(req, dict):
                raise TypeError("req must be a dict")

            if "config" not in req:
                raise ValueError("Missing required key: config")

            if not isinstance(req["config"], dict):
                raise TypeError("config must be a dict")
            
            if not isinstance(opt, dict):
                raise TypeError("opt must be a dict")
            
            if "user" not in opt:
                raise ValueError("Missing required key: user")
            
            if "user_email" not in opt:
                raise ValueError("Missing required key: user_email")
        except (TypeError, ValueError) as e:
            logging.error(str(e))
            return

        return {
            "taskId": req.get("taskId", ""),
            "status": req.get("status", ""),
            "user": {
                "email": opt.get("user_email", "")
            },
            "config": [
                {"name": req.get("config", "").get("name", "")},
                {"value": req.get("config", "").get("value", "")}
            ],
            "files": []
        }