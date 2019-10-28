from reprint import output
from .logger import Logger


class ConsoleLogger(Logger):
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

    def __init__(self, il=20):
        self.output_list = output(
            initial_len=il
        ).__enter__()

    def log(self, index, message):
        log_line = message.format()
        color = self.status_map[message.status]
        color = self.color_dict[color]
        log_line = '\033[;%dm[%3d]%s\033[0m' % (
            color, index, log_line
        )
        try:
            log_line = unicode(log_line, encoding='utf-8')
        except NameError: # python 2 compatibility
            pass
        self.output_list[index] = log_line
