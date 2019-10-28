from .file_logger import FileLogger
from .console_logger import ConsoleLogger
from multiprocessing import Process


class Board(Process):
    def __init__(self, result_queue, banners):
        super(Board, self).__init__()
        self.result_queue = result_queue
        self.banner = banners
        self.loggers = [
            ConsoleLogger(),
            FileLogger()
        ]

    index = []

    def dispatch(self, index, message):
        for i in self.loggers:
            i.log(index, message)

    def run(self):
        # for i in range(len(self.banner)):
        #     self.dispatch(i, '   ' + self.banner[i])
        while True:
            result = self.result_queue.get()
            if result.target not in self.index:
                self.index.append(result.target)
            index = self.index.index(result.target)
            self.dispatch(index, result)
