import logging
import os
import inspect

class AppLogger:
    __instance = None

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if AppLogger.__instance == None:
            AppLogger()
        return AppLogger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AppLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.setup()
            AppLogger.__instance = self


    def setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._set_file_handler()
        self._set_console_handler()
        
    @staticmethod 
    def get():
        return AppLogger.get_instance().logger


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
