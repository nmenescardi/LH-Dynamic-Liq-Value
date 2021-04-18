import logging
import os
import inspect

class AppLogger:
    def __init__(self):
               
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(filename='app.log',
                                           mode='a')
        
        caller_name = self._get_last_caller_file_name()
        fmt = '%(levelname)s: %(asctime)s - {}:%(lineno)d - %(message)s'.format(caller_name)
        formatter = logging.Formatter(fmt=fmt,
                                      datefmt='%d-%b-%y %H:%M:%S')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        self.logger = logger
        
    def get(self):
        return self.logger

    def _get_last_caller_file_name(self):
        return self._get_file_name_from_path(
            inspect.stack()[2].filename)
    
    def _get_file_name_from_path(self, path):
        return os.path.basename(path)
