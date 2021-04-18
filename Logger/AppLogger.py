import logging
import os
import inspect
from Helpers.Singleton import singleton

@singleton
class AppLogger:

    def __init__(self):
        self.setup()

    def setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._set_file_handler()
        self._set_console_handler()

    def get(self):
        return self.logger


    def _set_file_handler(self):
        fh = logging.FileHandler(filename='app.log',
                                           mode='a')
        fh.setLevel(logging.DEBUG)
        
        fmt = '%(levelname)s: %(asctime)s - %(filename)s:%(lineno)d - %(message)s'
        formatter = logging.Formatter(fmt=fmt,
                                      datefmt='%d-%b-%y %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)


    def _set_console_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter(fmt='%(levelname)s: - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
