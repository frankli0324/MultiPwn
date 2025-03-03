from reprint import output

from .logger import Logger, format_config


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
        'submit_error': 'red',
        'exploit_error': 'red'
    }
    success_count = 0

    def __init__(self):
        self.output_list = output(
            output_type='list'
        ).__enter__()

    def log(self, index, message):
        log_line = format_config.format(message, 'single_job')
        color = self.status_map[message.status]
        color = self.color_dict[color]
        log_line = '\033[;%dm[%3d]%s\033[0m' % (
            color, index, log_line
        )
        if message.status == 'success':
            self.success_count += 1
        try:
            log_line = unicode(log_line, encoding='utf-8')
        except NameError:  # python 2 compatibility
            pass
        if index >= len(self.output_list):
            self.output_list += [''] * (index - len(self.output_list) + 1)
        self.output_list[index] = log_line

    def clean_up(self):
        self.output_list.clear()
        print('finished')
        print('submitted %d correct flags in total' % self.success_count)
