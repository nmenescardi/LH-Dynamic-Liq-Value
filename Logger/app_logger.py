"""Module to hanlde app logging functionality"""

import logging

from helpers.singleton import singleton


@singleton
class AppLogger:  # pylint: disable=too-few-public-methods
    """Main Logger class to construct and retrieve the logger as a singleton object"""

    def __init__(self):
        self._setup()

    def _setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._set_file_handler()
        self._set_console_handler()

    def get(self):
        """Public method to get the logger"""
        return self.logger

    def _set_file_handler(self):
        file_handler = logging.FileHandler(filename="app.log", mode="a")
        file_handler.setLevel(logging.DEBUG)

        fmt = "%(levelname)s: %(asctime)s - %(filename)s:%(lineno)d - %(message)s"
        formatter = logging.Formatter(fmt=fmt, datefmt="%d-%b-%y %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _set_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
