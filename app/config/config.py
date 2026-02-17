from dynaconf import Dynaconf
import glob
import os

class Config:
    def __init__(self, env=None, pattern="./configs_default/*"):
        self.env = env or os.getenv('ENVIROMENT')
        self.pattern = pattern
        self.prompt_path = glob.glob(self.pattern, recursive=True)

        self._settings = Dynaconf(
            settings_file = self.prompt_path,
            default_env = self.env,
            enviroment = True
        )

        def get(self, key, default=None):
            return self._settings.get(key, default)

settings = Config()