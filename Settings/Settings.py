"""Module to handle default settings and script arguments"""
import argparse
from settings.config import default_config
from logger.app_logger import AppLogger


class Settings:  # pylint: disable=too-few-public-methods
    """Main Settings class"""

    def __init__(self, description=""):
        self.logger = AppLogger().get()
        self.parser = argparse.ArgumentParser(description)
        self._parse()

    def _parse(self):
        self.logger.debug("Parsing default config")
        self.logger.debug(default_config)

        for setting in default_config:
            self.parser.add_argument(setting.pop("arg"), **setting)
        self.args = vars(self.parser.parse_args())

    def get(self):
        """Public method to get the settings"""
        return self.args
