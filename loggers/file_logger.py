import logging
from .logger import Logger


class FileLogger(Logger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.FileHandler('exec.log'))
        self.logger.setLevel(logging.DEBUG)

    def log(self, index, message):
        self.logger.info(message.format())
