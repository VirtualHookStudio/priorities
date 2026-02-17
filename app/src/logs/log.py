from datetime import datetime
import logging

class Log():
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Log, cls).__new__(cls)
            cls.__instance.user = None
            cls.__instance.method = None
            cls.__instance.time_info = None
        return cls.__instance
    
    def set_user(self, user):
        try:
            if user is None:
                raise AttributeError("User instance cannot be None")
            self.user = user.get_user()
        except AttributeError as e:
            logging.error(str(e))

    def set_method(self, method):
        try:
            if method is None:
                raise AttributeError("Method cannot be None")
            self.method = method
        except AttributeError as e:
            logging.error(str(e))

    def set_time_info(self):
        date_info = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_info = date_info
    
    def get_user(self):
        return self.user

    def get_method(self):
        return self.method
    
    def get_time_info(self):
        return self.time_info
