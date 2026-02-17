import logging

from app.src.sites.generic_site import GenericSite

class siteCandleIo(GenericSite):
    def __init__(self):
        super().__init__("candleio")

    def _build_headers(self, req, opt):
        try:
            if not isinstance(opt, dict):
                raise TypeError("opt must be a dict")

            if "user" not in opt:
                raise ValueError("Missing required key: user")

            if not isinstance(opt["user"], dict):
                raise TypeError("user must be a dict")
        except (TypeError, ValueError) as e:
            logging.error(str(e))
            return
        
        return {
            "Content-Type": "application/json",
            "Authorizaton": req.get("Authorization")
        }
       

    def _build_payload(self, req, opt):
        return {
            "taskId": req.get("taskId", ""),
            "user": {
                "id": opt.get("user_id", "")
            },
            "files": req.get("files", "")
        }