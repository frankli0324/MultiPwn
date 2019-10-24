import logging
from multiprocessing import Process

from reprint import output


class Board(Process):
    def __init__(self, result_queue, banners: list):
        super().__init__()
        self.result_queue = result_queue
        self.output_list = []
        self.banner = banners
        self.file_logger = None

    color_dict = {
        "black": 30, "red": 31, "green": 32,
        "yellow": 33, "blue": 34, "goodred": 35,
        "greenblue": 36, "white": 37
    }
    status_map = {
        'starting': 'white',
        'attacking': 'white',
        'submitting': 'blue',
        'wrong': 'yellow',
        'success': 'green',
        'error': 'red',
    }
    index = []

    def log(self, result):
        log_line = result.format()
        color = self.status_map[result.status]
        color = self.color_dict[color]
        if result.target not in self.index:
            self.index.append(result.target)
        index = self.index.index(result.target)
        self.output_list[
            index + len(self.banner)
            ] = '\033[;%dm[%d]%s\033[0m' % (color, index + 1, log_line)
        self.file_logger.info(log_line)

    def run(self):
        __import__('os').system('clear')
        # , logging.getLogger(__name__) as log would be nice Orz
        with output(initial_len=20) as ol:
            log = logging.getLogger(__name__)
            log.addHandler(logging.FileHandler('exec.log'))
            self.output_list = ol
            self.file_logger = log
            log.setLevel(logging.DEBUG)
            for i in range(len(self.banner)):
                ol[i] = '   ' + self.banner[i]
            while True:
                result = self.result_queue.get()
                self.log(result)
        pass
