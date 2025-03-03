import logging
from .logger import Logger, format_config


class FileLogger(Logger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.FileHandler('exec.log'))
        self.logger.setLevel(logging.DEBUG)

    def log(self, index, message):
        self.logger.info(
            format_config.format(message, 'single_job')
        )
