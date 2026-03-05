from datetime import datetime

class Singletonmeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singletonmeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Log(metaclass=Singletonmeta):
    def __init__(self):
        self.user = None
        self.method = None
        self.time_info = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
