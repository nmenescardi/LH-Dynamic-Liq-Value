from Settings.Config import default_config
import argparse

class Settings:
    
    def __init__(self, description=''):
        self.parser = argparse.ArgumentParser(description)
        self._parse()

    def _parse(self):
        for setting in default_config:
            self.parser.add_argument(
                setting.pop('arg'),
                **setting
            )
        self.args = vars(self.parser.parse_args())

    def get(self):
        return self.args
