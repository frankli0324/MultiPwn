from multiprocessing import Process
from importlib import import_module


class PwnProcess(Process):
    def __init__(self, work_queue):
        super(PwnProcess, self).__init__()
        self.queue = work_queue

    def run(self):
        while True:
            work = self.queue.get()
            work.update_status('attacking')
            work.flag = import_module(
                '.'+work.exp, 'exp'
            ).attack(work.target)
            work.update_status('submitting')
