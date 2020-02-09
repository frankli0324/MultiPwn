from multiprocessing import Process

from .console_logger import ConsoleLogger
from .file_logger import FileLogger


class Logger(Process):
    def __init__(self, log_queue, *loggers):
        super(Logger, self).__init__()
        self.log_queue = log_queue
        self.loggers = loggers

    index = []

    def dispatch(self, index, message):
        for i in self.loggers:
            i.log(index, message)

    def run(self):
        try:
            while True:
                result = self.log_queue.get()
                if result.target not in self.index:
                    self.index.append(result.target)
                index = self.index.index(result.target)
                self.dispatch(index, result)
        except KeyboardInterrupt:
            for i in self.loggers:
                i.clean_up()
