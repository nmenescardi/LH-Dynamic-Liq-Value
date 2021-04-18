import argparse
from Settings.Config import default_config
from Logger.AppLogger import AppLogger

class Settings:
    
    def __init__(self, description=''):
        self.logger = AppLogger().get()
        self.parser = argparse.ArgumentParser(description)
        self._parse()

    def _parse(self):
        self.logger.debug('Parsing default config')
        self.logger.debug(default_config)

        for setting in default_config:
            self.parser.add_argument(
                setting.pop('arg'),
                **setting
            )
        self.args = vars(self.parser.parse_args())

    def get(self):
        return self.args
